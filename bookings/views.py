from .models import Rooms, Bookings  # Ensure these names match your models.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from hotels.models import Rooms
from django.db.models import Q
from .models import Bookings
from .forms import BookingForm
from django.views.generic import ListView
from django.contrib import messages


class BookingList(ListView):
    model = Bookings
    template_name = 'bookings/booking_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_queryset(self):
        queryset = Bookings.objects.all().order_by('check_in')

        query = self.request.GET.get('q')

        if query:

            queryset = queryset.filter(
                Q(email__icontains=query) |
                Q(room__number__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        page_obj = context['page_obj']  # kinukuha nya yung paginated by

        context.update({
            # para mas madali tawagin ginawang dictonary
            'current_page': page_obj.number,
            'last_page': page_obj.paginator.num_pages,
            'prev_num': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'next_num': page_obj.next_page_number() if page_obj.has_next() else None,
            'has_previous': page_obj.has_previous(),
            'has_next': page_obj.has_next(),
        })
        return context


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
