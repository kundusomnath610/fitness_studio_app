from django.db import models

# Create your models here.
#---------------------------

# Create the schema for Fitness Class Booking.
class FitnessClass(models.Model):
    CLASS_TYPES = [
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT')
    ]

    # Createing the field in SQLite
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=CLASS_TYPES)
    date = models.DateField()
    instructor = models.CharField(max_length=50)
    available_slots = models.PositiveIntegerField()

