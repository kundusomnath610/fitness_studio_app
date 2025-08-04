from django.db import models

# Create your models here.
#---------------------------

# Create the schema for Fitness Class And Booking.
class Fitness(models.Model):
    CLASS_TYPES = [
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT')
    ]

    # Createing the field in SQLite
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, choices=CLASS_TYPES)
    date = models.DateTimeField()
    instructor = models.CharField(max_length=50)
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} with {self.instructor} on {self.date}"

# This is Booking Field in SQLite
class Booking(models.Model):
    fitness = models.ForeignKey(Fitness, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.client_name} booked {self.fitness.name}"

