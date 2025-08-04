from django.shortcuts import render
from rest_framework import viewsets, status
from booking_api.models import Fitness, Booking
from booking_api.serializers import FitnessClassSerializers, BookingClassSerializers
from rest_framework.response import Response
from rest_framework.decorators import action
from datetime import datetime
import pytz

# # Create your views here.

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = Fitness.objects.all()
    serializer_class = FitnessClassSerializers

    def list(self, request, *args, **kwargs):
        tz_str = request.GET.get('tz', 'Asia/Kolkata')
        try:
            tz = pytz.timezone(tz_str)
        except pytz.UnknownTimeZoneError:
            return Response({"error": "Invalid timezone"}, status=400)

        classes = self.get_queryset()
        serializer = self.get_serializer(classes, many=True)
        data = serializer.data
        for item, instance in zip(data, classes):
            item['date'] = instance.date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        return Response(data)
    
class BookingClassViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingClassSerializers

    def create(self, request, *args, **kwargs):
        data = request.data

        # Use class_id to fetch fitness instance
        class_id = data.get("class_id")
        if not class_id or not data.get("client_name") or not data.get("client_email"):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fitness = Fitness.objects.get(id=class_id)
        except Fitness.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        if fitness.available_slots <= 0:
            return Response({"error": "No slots available"}, status=status.HTTP_409_CONFLICT)

        # Create booking manually and map to serializer
        booking = Booking.objects.create(
            fitness=fitness,
            client_name=data['client_name'],
            client_email=data['client_email']
        )

        fitness.available_slots -= 1
        fitness.save()

        booking.refresh_from_db()  # To populate booked_at

        serializer = BookingClassSerializers(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Custom Url filter By Client_email and Client_name using @action Decorator
    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.GET.get('client_name')
        email = request.GET.get('client_email')
        """
            Filter Store as a dictonary with Key And Value pair
        """
        filters = {}
        if name:
            filters['client_name__icontains'] = name
        if email:
            filters['client_email__iexact'] = email

        if not filters:
            return Response({"error": "Provide at least client_name or client_email"}, status=400)

        bookings = Booking.objects.filter(**filters)
        return Response(BookingClassSerializers(bookings, many=True).data)