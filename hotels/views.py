from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.urls import reverse
from django.db.models import Q
from .models import Rooms
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import ChangeRoom, AddRoom


class RoomList(ListView):
    model = Rooms
    template_name = 'hotels/room_list.html'
    context_object_name = 'rooms'
    paginate_by = 6

    def get_queryset(self):
        # lahat ng nasa category ay inorder by
        queryset = Rooms.objects.select_related(
            'category').all().order_by('number')

        query = self.request.GET.get('q')
        category_name = self.request.GET.get('type')
        available_only = self.request.GET.get("available")
        sorted_price = self.request.GET.get('sort')

        if query:
            # search filter pwede lang silang mag search ng room # at title
            queryset = queryset.filter(
                Q(number__icontains=query) |
                Q(category__title__icontains=query)
            )

        # filter by category
        if category_name:
            queryset = queryset.filter(category__title=category_name)

        # filter para di makita yung mga di available
        if available_only == '1':
            queryset = queryset.filter(is_available=True)

        # pang sort ng price
        if sorted_price == 'price_low':
            queryset = queryset.order_by('category__price_per_night')
        elif sorted_price == 'price_high':
            queryset = queryset.order_by('-category__price_per_night')

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


class RoomDetails(DetailView):
    model = Rooms
    template_name = 'hotels/room_details.html'
    context_object_name = 'room'


@staff_member_required
def change_room(request, room_id):

    # fetch yung room  tapos pag wala magsesend nang 404
    room = get_object_or_404(Rooms, id=room_id)

    if request.method == 'POST':
        # tinitingnan kung valid at saka sasave
        form = ChangeRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, "Room has been changed successfully.")
            # para bumalik sa roomlist
            return redirect('room-list')
        else:
            messages.error(
                request, 'Invalid Input: Please check if the info you inputted is correct')

    else:
        # para di gumawa si django ng bagong room at palitan lang yung room
        form = ChangeRoom(instance=room)

    return render(request, 'hotels/change_room.html', {'form': form, 'room': room})


@staff_member_required
def delete_room(request, room_id):
    room = get_object_or_404(Rooms, id=room_id)

    if request.method == 'POST':
        # 1. Capture info for the log BEFORE deleting
        room_number = room.number
        room_cat = room.category.title

        room.delete()

        messages.success(request, f"Room {room_number} has been deleted.")
        return redirect('room-list')

    # If they just try to visit the URL via GET, send them back
    return redirect('room-list')


@staff_member_required
def add_room(request):
    if request.method == 'POST':

        form = AddRoom(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "New room added to the inventory!")
            return redirect('room-list')
        else:
            form.add_error(None, 'Please check your input')
            messages.error(
                request, "Invalid data. Please check the red text below.")
    else:
        form = AddRoom()

    return render(request, 'hotels/add_room.html', {'form': form})
