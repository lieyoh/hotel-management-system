from .models import Rooms, Bookings  # Ensure these names match your models.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hotels.models import Rooms
from .models import Bookings
from .forms import BookingForm
from django.contrib import messages


def is_room_available(room, check_in, check_out):
    overlapping_bookings = Bookings.objects.filter(
        room=room,
        check_in__lt=check_out,
        check_out__gt=check_in,
    )
    return not overlapping_bookings.exists()


def create_booking(request):
    room_id = request.GET.get('room_id')
    room = get_object_or_404(Rooms, id=room_id)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            email = form.cleaned_data.get('email')
            check_in = booking.check_in
            check_out = booking.check_out

            # tignan kung yug email na yon ay nakapagbook na
            already_booked = Bookings.objects.filter(
                room=room,
                email=email,
                check_in=check_in,
                check_out=check_out
            ).exists()

            if already_booked:

                form.add_error(
                    None, "You have already booked a room for these dates!")

            elif not is_room_available(room, check_in, check_out):
                form.add_error(None, "Room is not available for these dates.")

            else:

                booking.email = email
                booking.room = room
                booking.save()
                return redirect('bookings:booking-payment', pk=booking.pk)
    else:
        form = BookingForm()

    return render(request, 'bookings/booking_form.html', {'form': form, 'room': room})


def payment_page(request, pk):
    booking = get_object_or_404(Bookings, pk=pk,)
    return render(request, 'bookings/booking_payment.html', {'booking': booking})
