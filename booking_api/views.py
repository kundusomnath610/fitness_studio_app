from django.shortcuts import render
from rest_framework import viewsets
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

#     def list(self, request, *args, **kwargs):
#         tz_str = request.GET.get('tz', 'Asia/Kolkata')
#         try:
#             tz = pytz.timezone(tz_str)
#         except pytz.UnknownTimeZoneError:
#             return Response({"error": "Invalid timezone"}, status=400)

#         classes = self.get_queryset()
#         serializer = self.get_serializer(classes, many=True)
#         data = serializer.data
#         for item, instance in zip(data, classes):
#             item['date'] = instance.date.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
#         return Response(data)
    
class BookingClassViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingClassSerializers

    def create(self, request, *args, **kwargs):
        data = request.data
        required = ['class_id', 'client_name', 'client_email']
        if not all(field in data for field in required):
            return Response({"error": "Missing required fields"}, status=400)

        try:
            fitness = Fitness.objects.get(id=data['class_id'])
        except Fitness.DoesNotExist:
            return Response({"error": "Class not found"}, status=404)

        if fitness.available_slots <= 0:
            return Response({"error": "No slots available"}, status=409)

        booking = Booking.objects.create(
            fitness=fitness,
            client_name=data['client_name'],
            client_email=data['client_email']
        )

        booking.refresh_from_db()

        fitness.available_slots -= 1
        fitness.save()
        return Response(BookingClassSerializers(booking).data, status=201)
    
    # Custom Url filter By email 
    @action(detail=False, methods=['get'])
    def by_email(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"error": "Email parameter required"}, status=400)
        bookings = Booking.objects.filter(client_email=email)
        return Response(BookingClassSerializers(bookings, many=True).data)
