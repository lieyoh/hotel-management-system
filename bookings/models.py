from django.db import models
from decimal import Decimal
from django.conf import settings
from hotels.models import Rooms
# Create your models here.


class Bookings(models.Model):
    email = models.EmailField(
        unique=False,
        max_length=255,
        verbose_name="Email Address"
    )
    room = models.ForeignKey(
        Rooms,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)
    reservation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # 1. para kahit less than 1 day yung reserve nila 1 day parin yung claculation
        delta = self.check_out - self.check_in
        days = delta.days
        if days <= 0:
            days = 1

        # Calculate the Total Price
        self.total_price = self.room.category.price_per_night * days

        # Calculate Reservation Fee (kailangan nila magbayad ng reservation fee at 20 percent ng total price)
        self.reservation_fee = self.total_price * Decimal('0.20')

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} - Room {self.room.number}"
