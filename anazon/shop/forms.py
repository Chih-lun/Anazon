from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailInput, ModelForm, PasswordInput, TextInput

from .models import Order, User


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
        labels = {
            "email": "Email",
            "password": "Password"
        }
        widgets = {
            "email":  EmailInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Your Email', 'autocomplete': 'off'}),
            "password": PasswordInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': '********', 'autocomplete': 'off', 'data-toggle': 'password'}),
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
        widgets = {
            "username":  EmailInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Email'}),
            "first_name": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'First Name'}),
            "last_name": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Last Name'}),
        }

    # for password1 and password2
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs\
            .update({
                'class': 'form-control form-control-lg',
                'required': 'required',
                'placeholder': '********',
            })
        self.fields['password2'].widget.attrs\
            .update({
                'class': 'form-control form-control-lg',
                'required': 'required',
                'placeholder': '********',
            })


class ShippingForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name',
                  'phone', 'email', 'postcode', 'address']
        labels = {
            "first_name": "",
            "last_name": "",
            "phone": "",
            "email": "",
            "postcode": "",
            "address": "",
        }
        widgets = {
            "first_name": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'First Name'}),
            "last_name": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Last Name'}),
            "phone": TextInput(attrs={'class': 'form-control form-control-lg', 'id': 'shipping_phone', 'required': 'required', 'placeholder': 'Phone', 'type': 'text'}),
            "email":  EmailInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Email', 'autocomplete': 'off'}),
            "postcode": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Postcode'}),
            "address": TextInput(attrs={'class': 'form-control form-control-lg', 'required': 'required', 'placeholder': 'Address'}),
        }
