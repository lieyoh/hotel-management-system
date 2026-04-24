from django.shortcuts import render
from .models import Rooms, RoomType
from django.views.generic import ListView
# Create your views here.


class RoomList(ListView):
    model = Rooms
    template_name = 'hotels/room_list.html'
    context_object_name = 'rooms'

    def get_queryset(self):
        queryset = Rooms.objects.select_related('category').all()
        return queryset
