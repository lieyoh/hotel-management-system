from django.urls import path
from . import views
from . views import BookingList
app_name = 'bookings'
urlpatterns = [
    path('booking_form/', views.create_booking, name='booking-form'),
    path('booking_list/', BookingList.as_view(), name='booking-list'),
    path('booking_payment/<int:pk>', views.payment_page, name='booking-payment'),
]
