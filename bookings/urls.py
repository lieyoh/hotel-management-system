from django.urls import path
from . import views

app_name = 'bookings'
urlpatterns = [
    path('booking_form/', views.create_booking, name='booking-form'),
    path('booking_payment/<int:pk>', views.payment_page, name='booking-payment'),
]
