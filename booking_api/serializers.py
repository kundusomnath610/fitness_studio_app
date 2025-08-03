from rest_framework import serializers
from booking_api.models import Fitness,Booking

"""
    Create Model Serializer for converting Object Data to JSON Format.
    Here are two Serializer for two model Data. One in Fitness Class And Another is Booking Class
"""

class FitnessClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fitness
        fields = '__all__'

class BookingClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

