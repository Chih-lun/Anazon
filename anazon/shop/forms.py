from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
