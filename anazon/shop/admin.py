from django.contrib import admin
from .models import Category, Product, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
