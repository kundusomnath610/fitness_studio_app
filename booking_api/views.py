from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from booking_api.models import Fitness, Booking
from booking_api.serializers import FitnessClassSerializers, BookingClassSerializers
from django.db import transaction
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from datetime import datetime, timezone


class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = Fitness.objects.all() # Queryset for Fitness classes
    serializer_class = FitnessClassSerializers

    def list(self, request, *args, **kwargs):
        tz_str = request.GET.get('tz', 'Asia/Kolkata')  # Default timezone

        try:
            tz = ZoneInfo(tz_str)
        except ZoneInfoNotFoundError:
            return Response({"error": "Invalid timezone"}, status=400)

        now_utc = datetime.now(timezone.utc)

        # Filter out past classes
        classes = self.get_queryset().filter(date__gte=now_utc)

        serializer = self.get_serializer(classes, many=True)
        data = serializer.data

        for item, instance in zip(data, classes):
            date_obj = instance.date
            if date_obj.tzinfo is None:
                date_obj = date_obj.replace(tzinfo=timezone.utc)

            item['date'] = date_obj.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')

        return Response(data)


class BookingClassViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingClassSerializers

    def create(self, request, *args, **kwargs):
        data = request.data
        required = ['class_id', 'client_name', 'client_email']
        if not all(field in data for field in required):
            return Response({"error": "Missing required fields"}, status=400)

        try:
            with transaction.atomic():
                fitness = Fitness.objects.select_for_update().get(id=data['class_id'])

                now_utc = datetime.now(timezone.utc)

                # Prevent booking for past classes
                if fitness.date < now_utc:
                    return Response({"error": "Cannot book a past class"}, status=400)

                # Check available slots
                if fitness.available_slots <= 0:
                    return Response({"error": "No slots available"}, status=409)

                booking = Booking.objects.create(
                    fitness=fitness,
                    client_name=data['client_name'],
                    client_email=data['client_email']
                )

                # Decrease available slots
                fitness.available_slots -= 1
                fitness.save()

                return Response(BookingClassSerializers(booking).data, status=201)

        except Fitness.DoesNotExist: # Handle case where class does not exist
            return Response({"error": "Class not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

    # Search bookings by client_name or client_email
    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.GET.get('client_name')
        email = request.GET.get('client_email')

        filters = {} # Initialize filters Dictionary
        if name:
            filters['client_name__icontains'] = name
        if email:
            filters['client_email__iexact'] = email

        if not filters:
            return Response({"error": "Provide at least client_name or client_email"}, status=400)

        bookings = Booking.objects.filter(**filters) # Apply filters to Booking model
        return Response(BookingClassSerializers(bookings, many=True).data) # Serialize and return the bookings
