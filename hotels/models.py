from django.db import models

# Create your models here.


class RoomType(models.Model):
    room_type = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10000, decimal_places=2)


class Rooms(models.Model):
    room_number = models.IntegerField(unique=True)
    category = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name='category')
    is_available = models.BooleanField(default=True)
    reason = models.CharField(max_length=100)
