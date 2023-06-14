from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.db.models import Q
from .models import Category, Product
from .forms import LoginForm, RegisterForm


def home(request):
    return render(request, 'shop/home.html', {})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if request.method == 'POST':
        # as defined in model. email is used to replace username
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            # redirect to the page before login
            return redirect(request.GET.get('next'))
        else:
            messages.error(
                request, ('Invalid email or password. Please Try Again!'))
            return redirect('login')
    return render(request, 'shop/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = RegisterForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')

    return render(request, 'shop/register.html', {'form': form})


def product(request):
    categories = Category.objects.all()

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    products = Product.objects.filter(Q(category__name__icontains=q))
    return render(request, 'shop/product.html', {'categories': categories, 'products': products})
