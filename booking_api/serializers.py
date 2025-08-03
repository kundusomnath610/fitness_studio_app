from rest_framework import serializers
from booking_api.models import Fitness

"""
    Create Model Serializer for converting Object Data to JSON Format.
    Here are two Serializer for two model Data
"""

class FitnessClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fitness
        fields = '__all__'

