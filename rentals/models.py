from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

# Registration Model (optional)
class Registration(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)  # Phone number stored as a string to handle various formats

    # Optional: Add more fields if needed (like full name, profile picture, etc.)
    # first_name = models.CharField(max_length=100, blank=True)
    # last_name = models.CharField(max_length=100, blank=True)

    def clean(self):
        # Simple password validation (e.g., minimum length, no spaces)
        if len(self.password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if re.search(r'\s', self.password):
            raise ValidationError("Password cannot contain spaces.")
        
        # Phone number validation (must contain only digits and be 10-15 digits long)
        if not re.match(r'^\+?[\d]{10,15}$', self.phone_number):
            raise ValidationError("Phone number must be between 10 and 15 digits and may include a leading '+'.")

        super().clean()

    def __str__(self):
        return f'{self.username} - {self.email}'
class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)  # Price per day
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)  # To track if the car is available for rent
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)  # Car image field

    def __str__(self):
        return f'{self.brand} {self.model} ({self.year})'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')  # Link to the user
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')  # Link to the car
    full_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15)
    rental_days = models.PositiveIntegerField()
    license = models.BooleanField()  # True for Yes, False for No
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking by {self.full_name} for {self.car.brand} {self.car.model}"
