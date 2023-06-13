from django.shortcuts import render, redirect
from .models import Category, Product
from .forms import LoginForm


def home(request):
    return render(request, 'shop/home.html', {})


def login(request):
    form = LoginForm()
    return render(request, 'shop/login.html', {'form': form})


def logout(request):
    return redirect('home')


def product(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'shop/product.html', {'categories': categories, 'products': products})
