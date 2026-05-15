from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm

# class ClientRegistrationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = User
#         # Isama lang ang fields na gusto mong i-input ng client
#         fields = ("username", "email", "first_name", "last_name")

class AdminUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        # Idinagdag natin ang 'role' sa listahan
        fields = ("username", "email", "first_name", "last_name", "role")

    # Optional: Pwede nating i-filter ang choices para hindi makagawa ang Admin ng isa pang 'ADMIN'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Kung gusto mong Manager, Staff, at Customer lang ang pwedeng gawin:
        self.fields['role'].choices = [
            (User.Role.MANAGER, 'Manager'),
            (User.Role.STAFF, 'Staff'),
            (User.Role.CUSTOMER, 'Customer'),
        ]