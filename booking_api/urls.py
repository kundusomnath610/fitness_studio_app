from django.contrib import admin
from django.urls import path, include
from booking_api.views import FitnessClassViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'classes', FitnessClassViewSet)

urlpatterns = [

    path('', include(router.urls))

]