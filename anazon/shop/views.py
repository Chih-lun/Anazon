from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django .core.paginator import Paginator, EmptyPage
from django.db.models import Q, Subquery
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
    # redirect to the page before login
    return redirect(request.GET.get('next'))


def register(request):
    form = RegisterForm(request.POST)

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'shop/register.html', {'form': form})


def product(request):
    catergories = Category.objects.all()

    search = request.GET.get('search') if request.GET.get(
        'search') != None else ''
    if not search:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(title__icontains=search))

    # get related categories
    tags = Category.objects.filter(pk__in=Subquery(
        products.values("category")))

    tag = request.GET.get('tag') if request.GET.get(
        'tag') != None else ''

    if tag:
        products = products.filter(Q(category__name__iexact=tag))

    paginator = Paginator(products, 9)

    # convert page into int
    try:
        page_num = int(request.GET.get('page', 1))
    except ValueError:
        page_num = 1

    # avoid not-existing page
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    return render(request, 'shop/product.html', {'categories': catergories, 'tags': tags, 'products': page})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


def cart_detail(request):
    '''mainly controlled by frontend'''
    return render(request, 'shop/cart_detail.html', {})


@require_http_methods("POST")
def checkout(request):
    ''' POST ONLY METHOD '''
    if not request.user.is_authenticated:
        return redirect('/login/?next=/cart_detail/')

    cart_items = dict(request.POST)
    del cart_items['csrfmiddlewaretoken']
    print(cart_items)

    return HttpResponse('success')
