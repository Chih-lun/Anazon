from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    # Use email to login
    username = models.EmailField(unique=True, null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255, null=False)
    price = models.FloatField(null=False)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    image = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    # phone = PhoneNumberField(null=False, blank=False)
    pass


class OrderItem(models.Model):
    # title = models.CharField(max_length=255, null=False)
    # price = models.FloatField(null=False)
    # image = models.TextField(null=True, blank=True)
    # updated = models.DateTimeField(auto_now=True)
    # created = models.DateField(auto_now_add=True)
    # product = models.ForeignKey(Product, on_delete=models.SET_NULL)

    # def __str__(self):
    #     return self.title
    pass
