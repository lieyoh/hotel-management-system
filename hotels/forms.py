from django import forms
from .models import Rooms


class ChangeRoom(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['is_available', 'reason']
        widgets = {
            'reason': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-red-500'})
        }


class AddRoom(forms.ModelForm):
    class Meta:
        model = Rooms
        fields = ['number', 'category', 'is_available', 'reason']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-red-500'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-red-500'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-red-600 rounded'}),
            'reason': forms.Select(attrs={'class': 'w-full px-4 py-2 border rounded-lg outline-none focus:ring-2 focus:ring-red-500'}),
        }
