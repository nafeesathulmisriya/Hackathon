from django.http import HttpResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout
from .models import Car,Booking
import re
from decimal import Decimal
from django.template.loader import get_template

# Index view
def index(request):
    return render(request, "index.html")

# Registration view
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone_number = request.POST['phonenumber']

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered")
            return redirect('register')

        # Check if the password is valid
        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
            return redirect('register')

        if re.search(r'\s', password):
            messages.error(request, "Password cannot contain spaces")
            return redirect('register')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Your account has been successfully created')
        return redirect('login')

    return render(request, "register.html")

# Login view
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate the user using the email
        try:
            user = User.objects.get(email=email)  # Get the user object using email
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                # Successful login
                auth_login(request, user)
                messages.success(request, "You have logged in successfully!")
                return redirect('home')  # Redirect to the home page
            else:
                messages.error(request, "Invalid email or password.")
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

        return redirect('login')  # Redirect back to login page if authentication fails

    return render(request, "login.html")

# Logout view
def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect('index')

# Home page view)  # Redirects to login page if user is not logged in
def home(request):
    cars = Car.objects.filter(available=True)  # Fetch only available cars
    return render(request, 'home.html', {'cars': cars}) 

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Car, Booking

@login_required
def home(request):
    cars = Car.objects.all()  # Get all available cars
    return render(request, 'home.html', {'cars': cars})

@login_required
def booking(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mobile_number = request.POST['mobile_number']
        rental_days = int(request.POST['rental_days'])
        license = request.POST.get('license', False) == 'on'  # Checkbox is checked if 'on'
        
        # Calculate total cost
        total_cost = car.price_per_day * rental_days
        
        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            car=car,
            full_name=full_name,
            mobile_number=mobile_number,
            rental_days=rental_days,
            license=license,
            total_cost=total_cost
        )
        
        return redirect('payment',rental_id=car_id)  # Redirect to the home page after successful booking
    
    return render(request, 'booking.html', {'car': car})
def payment(request, rental_id):
    # Fetch the booking and related car details
    booking = get_object_or_404(Booking, id=rental_id)
    car = booking.car
    
    # Calculate total cost if not already calculated
    rental_days = booking.rental_days
    total_cost = car.price_per_day * rental_days
    
    # Add context for the template
    context = {
        'car': car,
        'rental_days': rental_days,
        'price_per_day': car.price_per_day,
        'total_cost': total_cost,
        'full_name': booking.full_name,
        'mobile_number': booking.mobile_number,
    }

    if request.method == 'POST':
        # Here you would handle actual payment logic (e.g., integrating with Stripe or PayPal)
        # For now, we'll simulate payment success
        
        # Mark the booking as confirmed and update the car availability
        booking.status = 'confirmed'
        booking.save()

        # Update car availability back to true
        car.available = True
        car.save()

        # Show success message
        messages.success(request, "Your booking has been confirmed!")

        # Redirect to the home page or any other page
        return redirect('success')

    return render(request, 'payment.html', context)

def success(request):
    return render(request,"success.html")
