from django.contrib import admin
from django.urls import path, include
from booking_api.views import FitnessClassViewSet, BookingClassViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'classes', FitnessClassViewSet)
router.register(r'book', BookingClassViewSet)

urlpatterns = [

    path('', include(router.urls))

]