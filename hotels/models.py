from django.db import models

# Create your models here.


class RoomType(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10000, decimal_places=2)

    def __str__(self):
        return self.title


Reason_choices = [
    ('Maintenance', 'Maintenance'),
    ('Occupied', 'Occupied'),
    ('Available', 'Available'),
    ('Out of Order', 'Out of Order'),
]


class Rooms(models.Model):

    number = models.IntegerField(unique=True)
    category = models.ForeignKey(
        RoomType, on_delete=models.CASCADE, related_name='category')
    is_available = models.BooleanField(default=True)
    reason = models.CharField(
        max_length=20,
        choices=Reason_choices,
        default='Available',
        verbose_name='Reasons - Maintenance, Occupied, Available, Out of Order'
    )

    def __str__(self):
        return f"Room {self.number} - {self.category.title}"
