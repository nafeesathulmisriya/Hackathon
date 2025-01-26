

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),  # Ensure this is defined
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('booking/<int:car_id>/', views.booking, name='booking'),
    path('payment/<int:rental_id>/', views.payment, name='payment'),
    path('payment/successful/', views.success, name='success'),


]
