from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django .core.paginator import Paginator, EmptyPage
from django.db.models import Q, Subquery
from .models import Category, Product, Order, User
from .forms import LoginForm, RegisterForm
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


def home(request):
    # print(stripe.checkout.Session.list())
    # line_items = stripe.checkout.Session.list_line_items(
    #     'cs_test_b1KpUoBBITqsjawISpEo0ZnZz8TkoB3AOQOOMbuIzgamtDIu3wchGUOaiq')
    # print(line_items)
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


@login_required(login_url='/login/')
def order(request):
    orders = Order.objects.filter(user=request.user).all()
    paginator = Paginator(orders, 10)

    # convert page into int
    try:
        page_num = int(request.GET.get('page', 10))
    except ValueError:
        page_num = 1

    # avoid not-existing page
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    return render(request, 'shop/order.html', {'orders': page})


@login_required(login_url='/login/')
def order_detail(request, stripe_id):
    order = Order.objects.get(stripe_id=stripe_id)
    line_items = stripe.checkout.Session.list_line_items(order.stripe_id)[
        'data']
    order_items = [{'product': stripe.Product.retrieve(line_item['price']['product']), 'price': line_item['price']['unit_amount'],
                    'quantity': line_item['quantity']} for line_item in line_items]
    order_items = [{'pk': order_item['product']['metadata']['pk'], 'title':order_item['product']['name'], 'image':order_item['product']['images']
                    [0], 'price': format(float(order_item['price'])/100, '.2f'), 'quantity': order_item['quantity']} for order_item in order_items]

    return render(request, 'shop/order_detail.html', {'order': order, 'order_items': order_items})


def cart_detail(request):
    '''mainly controlled by frontend'''
    return render(request, 'shop/cart_detail.html', {})


@require_http_methods("POST")
def checkout_redirect(request):
    ''' POST ONLY METHOD TO HANDLE CART ITEMS FROM FRONTEND AND REDIRECT IT TO CONFIRM FORM'''
    if not request.user.is_authenticated:
        return redirect('/login/?next=/cart_detail/')

    # cart_items example [('20', ['1']), ('19', ['2'])]
    cart_items = dict(request.POST)
    del cart_items['csrfmiddlewaretoken']
    request.session['cart_items'] = json.dumps(cart_items)
    # cart_items = [Product.objects.get(id=cart_item[0])
    #               for cart_item in cart_items.items()]

    return redirect('checkout')


def checkout(request):
    if not request.META.get('HTTP_REFERER') or not (request.META.get('HTTP_REFERER') ==
                                                    request.build_absolute_uri(reverse('checkout')) or
                                                    request.META.get('HTTP_REFERER') ==
                                                    request.build_absolute_uri(reverse('cart_detail'))):
        raise HttpResponseForbidden()

    # cart_items example [(<Product: Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin>, '1'),
    #  (<Product: Opna Women's Short Sleeve Moisture>, '2')]
    cart_items = json.loads(request.session['cart_items'])
    cart_items = [{'product': Product.objects.get(id=cart_item[0]), 'quantity':cart_item[1][0]}
                  for cart_item in cart_items.items()]

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        line_items = []
        for cart_item in cart_items:
            product = cart_item['product']
            quantity = cart_item['quantity']
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(product.price * 100),
                    'product_data': {
                        'name': product.title,
                        'description': product.description,
                        'images': [product.image],
                        'metadata': {
                            'pk': product.pk,
                        }
                    },
                },
                'quantity': quantity,
            })

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=[
                    'card',
                ],
                line_items=line_items,
                metadata={
                    "user_pk": request.user.pk,
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "email": email,
                    "postcode": postcode,
                    "address": address,
                },
                mode='payment',
                success_url=request.build_absolute_uri(
                    reverse('success')) + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=request.build_absolute_uri(reverse('cancel')),
            )
        except:
            return HttpResponse('error')

        return redirect(checkout_session.url, code=303)

    return render(request, 'shop/checkout.html', {'cart_items': cart_items})


# for local order model
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    # You can find your endpoint's secret in your webhook settings
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    if (event['type'] == 'checkout.session.completed'):
        user_pk = event['data']['object']['metadata']['user_pk']
        stripe_id = event['data']['object']['id']
        first_name = event['data']['object']['metadata']['first_name']
        last_name = event['data']['object']['metadata']['last_name']
        phone = event['data']['object']['metadata']['phone']
        email = event['data']['object']['metadata']['email']
        postcode = event['data']['object']['metadata']['postcode']
        address = event['data']['object']['metadata']['address']
        Order.objects.create(
            user=User.objects.get(pk=user_pk),
            stripe_id=stripe_id,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            postcode=postcode,
            address=address
        )

    # Passed signature verification
    return HttpResponse(status=200)


def success(request):
    return render(request, 'shop/success.html', {})


def cancel(request):
    return render(request, 'shop/cancel.html', {})
