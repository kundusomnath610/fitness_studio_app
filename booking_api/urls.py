from django.contrib import admin
from django.urls import path, include
from booking_api.views import FitnessClassViewSet, BookingClassViewSet
from rest_framework import routers

router = routers.DefaultRouter() # Default router for API endpoints
router.register(r'classes', FitnessClassViewSet) # Registering FitnessClassViewSet with the router
router.register(r'book', BookingClassViewSet) # Registering BookingClassViewSet with the router

# URL patterns for the booking API
urlpatterns = [

    path('', include(router.urls))

]