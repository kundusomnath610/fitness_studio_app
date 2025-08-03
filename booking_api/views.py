from django.shortcuts import render
from rest_framework import viewsets
from booking_api.models import Fitness
from booking_api.serializers import FitnessClassSerializers
from rest_framework.response import Response
from datetime import datetime
import pytz

# Create your views here.

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = Fitness.objects.all()
    serializer_class = FitnessClassSerializers

    def list(self, request, *args, **kwargs):
        tz_str = request.GET.get('tz', 'Asia/Bangalore')
        try:
            tz = pytz.timezone(tz_str)
        except pytz.UnknownTimeZoneError:
            return Response({"error": "Invalid timezone"}, status=400)

        classes = self.get_queryset()
        serializer = self.get_serializer(classes, many=True)
        data = serializer.data
        for item, instance in zip(data, classes):
            item['datetime'] = instance.datetime.astimezone(tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        return Response(data)
