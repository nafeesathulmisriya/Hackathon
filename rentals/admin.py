from django.contrib import admin
from rentals.models import Booking, Registration,Car

# Register your models here.
admin.site.register(Registration)
admin.site.register(Car)
admin.site.register(Booking)