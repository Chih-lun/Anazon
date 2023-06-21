from django.forms import ModelForm, EmailInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        labels = {
            "email": "Email",
            "password": "Password"
        }
        widgets = {
            "email":  EmailInput(attrs={'placeholder': 'email', 'autocomplete': 'off'}),
            "password": PasswordInput(attrs={'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        labels = {
            "username": "Email",
        }
        help_texts = {
            'password': None,
        }
