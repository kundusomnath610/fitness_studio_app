import re
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from booking_api.models import Fitness, Booking
from booking_api.serializers import FitnessClassSerializers, BookingClassSerializers
from django.db import transaction
from loguru import logger
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import datetime, timezone

logger = logger.bind(name="booking_views")
logger.info("Booking request received")
logger.warning("Invalid timezone: Asia/XYZ")
logger.error("Missing required fields")
logger.success("Booking successful")
logger.exception("Unexpected error during booking")


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"  # Simple email format check

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = Fitness.objects.all()
    serializer_class = FitnessClassSerializers

    def list(self, request, *args, **kwargs):
        tz_str = request.GET.get('tz', 'Asia/Kolkata')
        logger.info(f"Timezone received: {tz_str}")

        try:
            tz = ZoneInfo(tz_str)
        except ZoneInfoNotFoundError:
            logger.warning(f"Invalid timezone: {tz_str}")
            return Response({"error": "Invalid timezone"}, status=400)

        now_utc = datetime.now(timezone.utc)
        classes = self.get_queryset().filter(date__gte=now_utc)
        serializer = self.get_serializer(classes, many=True)
        data = serializer.data

        for item, instance in zip(data, classes):
            date_obj = instance.date
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=timezone.utc)
            item['date'] = date_obj.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')

        logger.info(f"Returned {len(data)} upcoming classes")
        return Response(data)


class BookingClassViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingClassSerializers

    def create(self, request, *args, **kwargs):
        data = request.data
        logger.info(f"Booking request received: {data}")

        required = ['class_id', 'client_name', 'client_email']
        if not all(field in data for field in required):
            logger.error("Missing required fields in booking request")
            return Response({"error": "Missing required fields"}, status=400)

        if not isinstance(data['class_id'], int):
            logger.error("Invalid class_id type")
            return Response({"error": "class_id must be an integer"}, status=400)

        if not re.match(EMAIL_REGEX, data['client_email']):
            logger.error(f"Invalid email format: {data['client_email']}")
            return Response({"error": "Invalid email format"}, status=400)

        try:
            with transaction.atomic():
                fitness = Fitness.objects.select_for_update().get(id=data['class_id'])

                now_utc = datetime.now(timezone.utc)
                if fitness.date < now_utc:
                    logger.warning(f"Attempt to book past class ID {fitness.id}")
                    return Response({"error": "Cannot book a past class"}, status=400)

                if fitness.available_slots <= 0:
                    logger.warning(f"No slots available for class ID {fitness.id}")
                    return Response({"error": "No slots available"}, status=409)

                booking = Booking.objects.create(
                    fitness=fitness,
                    client_name=data['client_name'],
                    client_email=data['client_email']
                )

                fitness.available_slots -= 1
                fitness.save()

                logger.success(f"Booking successful for class ID {fitness.id} by {data['client_email']}")
                return Response(BookingClassSerializers(booking).data, status=201)

        except Fitness.DoesNotExist:
            logger.error(f"Class ID {data['class_id']} not found")
            return Response({"error": "Class not found"}, status=404)
        except Exception as e:
            logger.exception("Unexpected error during booking")
            return Response({"error": str(e)}, status=500)

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.GET.get('client_name')
        email = request.GET.get('client_email')
        filters = {}

        if name:
            filters['client_name__icontains'] = name
        if email:
            filters['client_email__iexact'] = email

        if not filters:
            logger.error("Search request missing client_name or client_email")
            return Response({"error": "Provide at least client_name or client_email"}, status=400)

        bookings = Booking.objects.filter(**filters)
        logger.info(f"Found {bookings.count()} bookings matching filters: {filters}")
        return Response(BookingClassSerializers(bookings, many=True).data)
