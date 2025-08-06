📘 Introduction
Fitness Class Booking API is a Django-based RESTful web service designed to manage fitness class schedules and client bookings. The API allows users to:

View a list of upcoming fitness classes with details like type, date, instructor, and available slots.

Book a slot in a fitness class by providing their name and email.

Ensure real-time slot availability and prevent overbooking.

Search for existing bookings using either the client’s name or email address.

This system is ideal for fitness centers, gyms, or yoga studios looking to digitize their class scheduling and customer management. Built using Django and Django REST Framework (DRF), it provides scalable architecture and can be easily extended with features like authentication, payment gateways, email confirmations, or admin dashboards.(Future Extendation)

🏋️‍♂️ Fitness Class Booking API (Django + Django REST Framework)
This project is a Django-based RESTful API for managing Fitness Classes and Client Bookings. It allows users to:

View upcoming fitness classes
Book a class (with slot validation)
Search bookings by client name or email
🔧 Tech Stack
Python 3.13.2
Django 5.2.4
Django REST Framework 3.16.0
SQLite 3 (default, can be switched to PostgreSQL/MySQL)
Docker Desktop (For Contenarization)
📁 Project Structure
Screenshot 2025-08-06 at 12 19 49
⚙️ Setup Instructions
1. 📥 Clone the Repository
git clone https://github.com/kundusomnath610/fitness_studio_app
Then Change the Dir

cd booking_api_project
🐍 Create Virtual Environment(If needed, But it Highly Recomended to create .venv to avoid
 python3 -m venv env
 source env/bin/activate  # On Windows: env\Scripts\activate
📦 Install Dependencies
 pip install -r requirements.txt

If requirements.txt is missing, install manually: then

pip install django djangorestframework pytz

🔐 Apply Migrations
For Windows
python manage.py makemigrations
python manage.py migrate
For Mac/ Linux use instade of Python Use Python3

▶️ Run the Server
For Windows
python manage.py runserver
for Mac/Linux
python3 manage.py runserver
Note:- If you get port related error and change the port number (ex. python3 manage.py runserver 9000 -> new port)
🔍 API Endpoints
Method	Endpoint	Description
GET	/classes/	List upcoming fitness classes
POST	/book/	Book a class by class_id, name, email
GET	/book/search/	Filter bookings by client_name or client_email
📦 Example POST Request (Booking)
 POST /book/
 {
   "class_id": 1,
   "client_name": "John Doe",
   "client_email": "john@example.com"
 }
✅ Running Unit Tests
 python manage.py test
🧪 Sample Test Case (tests.py)
from django.test import TestCase
from booking_api.models import Fitness, Booking
from django.utils import timezone

class FitnessModelTest(TestCase):
    def test_create_class(self):
        fitness = Fitness.objects.create(
            name='Yoga',
            date=timezone.now(),
            instructor='Alex',
            available_slots=10
        )
        self.assertEqual(fitness.name, 'Yoga')
        self.assertEqual(fitness.available_slots, 10)
Docker File and Docker-Compose.yml
Run the build command

docker build -t <your_container_name> (ex. booking_app in my case)
Expose port:- 8000:8000 (Write in your Docker File not in Terminal)
🚀 Future Scope
Some features to add in the next versions:

✅ User authentication (login, register)

✅ Class cancellation & refund logic

✅ Email notifications for booking

✅ Pagination, sorting & filtering on endpoints

✅ Admin dashboard (optional: Django Admin or React Frontend)

✅ Switching to PostgreSQL in production

✅ Rate limiting and security enhancements

📫 Contact
For queries or contributions, reach out to:

📧 Mail:- kundusomnath610@gmail.com

💼 LinkedIn Profile :- https://www.linkedin.com/in/somnath-kundu/

🌐 GitHub Profile:- https://github.com/kundusomnath610
