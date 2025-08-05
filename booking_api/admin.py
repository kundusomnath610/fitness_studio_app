from django.contrib import admin
from booking_api.models import Fitness, Booking

# Display the field in admin site for Fitness Model
class FitnessAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'available_slots', 'date') # Display fields in admin site
    search_fields = ['name', 'instructor'] # Search by name and instructor
# Display the field in admin site for Booking Model
class BookinAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'client_email', 'booked_at') # Display fields in admin site
    list_filter = ['client_name', 'client_email'] # Search by name and Email
    


# Register your models here for Admin.
admin.site.register(Fitness, FitnessAdmin) 
admin.site.register(Booking, BookinAdmin)
