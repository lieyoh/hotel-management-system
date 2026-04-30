from django.urls import path
from .views import RoomList, RoomDetails
from . import views


urlpatterns = [
    path('room_list/', RoomList.as_view(), name='room-list'),
    path('room_detail/<int:pk>/', RoomDetails.as_view(), name='room-detail'),
    path('change_room/<int:room_id>/', views.change_room, name='change-room'),
    path('add_room/', views.add_room, name='add-room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete-room'),
]
