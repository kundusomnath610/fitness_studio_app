from django.test import TestCase
from rest_framework.test import APIClient
from booking_api.models import Fitness, Booking
from django.utils.timezone import now, timedelta
from rest_framework import status
import pytz

# Create your tests here.

# API test Case for Create 
class BookingAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.fitness_class = Fitness.objects.create(
            name='Yoga',
            date=now() + timedelta(days=1),
            instructor='Jane Doe',
            available_slots=5
        )
    
    # Time Zone test case 
    def test_fitness_list_with_timezone(self):
        response = self.client.get('/get/classes/?tz=Asia/Kolkata')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('date', response.json()[0])

    # Test Case for missing Fields for Booking
    def test_create_booking_missing_fields(self):
        response = self.client.post('/post/book/', {
            'client_name': 'Alice'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # If Booking class_id is not Present the database then return 404 not_found
    def test_create_booking_class_not_found(self):
        response = self.client.post('/post/book/', {
            'class_id': 999,  # invalid
            'client_name': 'Bob',
            'client_email': 'bob@example.com'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # If available_slot is not present then booking will be not happen
    def test_create_booking_no_slots(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        response = self.client.post('/post/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'Carol',
            'client_email': 'carol@example.com'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # Test for successfully booking User
    def test_create_booking_success(self):
        response = self.client.post('/post/book/', {
            'class_id': self.fitness_class.id,
            'client_name': 'David',
            'client_email': 'david@example.com'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Fitness.objects.get(id=self.fitness_class.id).available_slots, 4)

    # Test case for searching by email
    def test_search_booking_by_email(self):
        Booking.objects.create(
            fitness=self.fitness_class,
            client_name='Emily',
            client_email='emily@example.com'
        )
        response = self.client.get('/post/book/search/?client_email=emily@example.com')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # Test case for Search by name 
    def test_search_booking_by_name(self):
        Booking.objects.create(
            fitness=self.fitness_class,
            client_name='Frank',
            client_email='frank@example.com'
        )
        response = self.client.get('/post/book/search/?client_name=frank')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    # Test case for search with out params(name, email)
    def test_search_booking_no_query(self):
        response = self.client.get('/post/book/search/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)