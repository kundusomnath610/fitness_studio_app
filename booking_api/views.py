from django.shortcuts import render
from rest_framework import viewsets
from booking_api.models import Fitness
from booking_api.serializers import FitnessClassSerializers

# Create your views here.

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = Fitness.objects.all()
    serializer_class = FitnessClassSerializers
