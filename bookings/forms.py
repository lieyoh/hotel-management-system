from django import forms
from .models import Bookings
from django.utils import timezone
from django.core.exceptions import ValidationError


class BookingForm(forms.ModelForm):
    class Meta:
        model = Bookings
        fields = ['email', 'check_in', 'check_out']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500', 'placeholder': 'your@email.com'}),
            'check_in': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500'}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-red-500'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # This line removes the 'unique' check so your view can handle the logic instead
        self.fields['email']._unique_check = False

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            # Bawal ang past dates
            if check_in < timezone.now().date():
                raise ValidationError(
                    "Check-in date cannot be in the past!")

            # Bawal ang check-out before check-in
            if check_out <= check_in:
                raise ValidationError(
                    "Check-out date must be after the check-in date.")

        return cleaned_data
