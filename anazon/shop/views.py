from django.shortcuts import render, redirect, reverse, HttpResponse
from django.http import HttpResponseForbidden, JsonResponse, Http404
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
    ''' HOME PAGE'''
    return render(request, 'shop/home.html', {})


def user_login(request):
    ''' USER LOGIN '''

    # restrict the authenticated user
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm()
    if request.method == 'POST':
        # as defined in model. email is used to replace username
        email = request.POST.get('email')
        password = request.POST.get('password')

        # user authentication
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
    ''' USER LOGOUT '''

    logout(request)
    # redirect to the page before login
    return redirect(request.GET.get('next'))


def register(request):
    ''' USER REGISTRATION '''

    form = RegisterForm(request.POST)

    # restrict the authenticated user
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        # store user information to database
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'shop/register.html', {'form': form})


def product(request):
    ''' DISPLAY ALL THE PRODUCTS '''

    search = request.GET.get('search') if request.GET.get(
        'search') != None else ''

    # if user does input search, find all the products
    if not search:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(
            Q(title__icontains=search))

    category = request.GET.get('category') if request.GET.get(
        'category') != None else ''
    if category:
        products = products.filter(Q(category__name__iexact=category))

    # get related tags
    tags = Category.objects.filter(pk__in=Subquery(
        products.values("category")))

    tag = request.GET.get('tag') if request.GET.get(
        'tag') != None else ''

    # if user select a tag, filter the related products
    if tag:
        products = products.filter(Q(category__name__iexact=tag))

    # pagination
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

    return render(request, 'shop/product.html', {'tags': tags, 'products': page})


def product_detail(request, pk):
    ''' DISPLAY PRODUCT DETAIL '''

    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        raise Http404(f'the product_id {pk} does not exist!')

    return render(request, 'shop/product_detail.html', {'product': product})


@login_required(login_url='/login/')
def order(request):
    ''' DISPLAY ALL THE ORDERS '''

    # find all the orders
    orders = Order.objects.filter(user=request.user).all()
    # pagination
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
    ''' DISPLAY ORDER DETAIL '''

    try:
        order = Order.objects.get(stripe_id=stripe_id)
    except Order.DoesNotExist:
        raise Http404(f'the stripe_id {stripe_id} does not exist!')

    # find line_items from stripe checkout session
    line_items = stripe.checkout.Session.list_line_items(order.stripe_id)[
        'data']

    # restructure the order_items from line_items
    order_items = [{'product': stripe.Product.retrieve(line_item['price']['product']), 'price': line_item['price']['unit_amount'],
                    'quantity': line_item['quantity']} for line_item in line_items]
    order_items = [{'pk': order_item['product']['metadata']['pk'], 'title':order_item['product']['name'], 'image':order_item['product']['images']
                    [0], 'price': format(float(order_item['price'])/100, '.2f'), 'quantity': order_item['quantity']} for order_item in order_items]

    return render(request, 'shop/order_detail.html', {'order': order, 'order_items': order_items})


def cart_detail(request):
    ''' CONTROLLED BY FRONTEND TO DISPLAY USER'S CART ITEM '''
    return render(request, 'shop/cart_detail.html', {})


@require_http_methods("POST")
def checkout_redirect(request):
    ''' POST ONLY METHOD TO HANDLE CART ITEMS FROM FRONTEND AND REDIRECT IT TO SHIPMENT FORM '''

    # check user login
    if not request.user.is_authenticated:
        return redirect('/login/?next=/cart_detail/')

    # cart_items example [('20', ['1']), ('19', ['2']), ('csrfmiddlewaretoken': 'csrfmiddlewaretoken')]
    cart_items = dict(request.POST)
    del cart_items['csrfmiddlewaretoken']
    # store cart item in session
    request.session['cart_items'] = json.dumps(cart_items)

    return redirect('checkout')


def checkout(request):
    ''' GET METHOD TO RENDER SHIPMENT FORM AND POST METHOD TO REDIRECT TO STRIPE PAYMENT '''

    # prevent direct access. it can only be accessed by "checkout" or "cart_detail"
    if not request.META.get('HTTP_REFERER') or not (request.META.get('HTTP_REFERER') ==
                                                    request.build_absolute_uri(reverse('checkout')) or
                                                    request.META.get('HTTP_REFERER') ==
                                                    request.build_absolute_uri(reverse('cart_detail'))):
        raise HttpResponseForbidden()

    # load cart from session and parse it into json
    try:
        cart_items = json.loads(request.session['cart_items'])
    except:
        # if cart is empty raise error
        raise HttpResponseForbidden()

    # then refine it. cart_items example [(<Product: Acer SB220Q bi 21.5 inches Full HD (1920 x 1080) IPS Ultra-Thin>, '1'),
    #  (<Product: Opna Women's Short Sleeve Moisture>, '2')]
    cart_items = [{'product': Product.objects.get(pk=cart_item[0]), 'quantity':cart_item[1][0]}
                  for cart_item in cart_items.items()]

    if request.method == 'POST':
        # shipment details
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        postcode = request.POST.get('postcode')
        address = request.POST.get('address')
        # get its form in line_items, so it can be passed to stripe payment
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

        # create checkout session
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
            # unexpected error
            return HttpResponse(status=500)

        # redirect it to stripe payment
        return redirect(checkout_session.url, code=303)

    # render shipment form
    return render(request, 'shop/checkout.html', {'cart_items': cart_items})


@csrf_exempt
def stripe_webhook(request):
    ''' STRIPE WEBHOOK TO LISTEN TRANSACTION, SO IT CAN BE APPENDED INTO DATABASE '''

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

    # when stripe payment is completed, then add it to database
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
    ''' STRIPE PAYMENT IS SUCCESSFUL '''

    session_id = request.GET.get('session_id')

    # if there is no related session_id, it will restrict the user access
    try:
        stripe.checkout.Session.retrieve(session_id)
    except:
        return HttpResponseForbidden()

    # set the flag to clean localstorage in session, so frontend can be notified by get method "clear_localstorage"
    request.session['clear_localstorage'] = True
    return render(request, 'shop/success.html', {'session_id': session_id})


def cancel(request):
    ''' STRIPE PAYMENT IS CANCEL '''

    return render(request, 'shop/cancel.html', {})


def get_categories(request):
    '''GET METHOD TO TELL FRONTEND ALL CATEGORIES SO IT CAN BE DISPLAYED IN NAVBAR'''
    categories = Category.objects.all()
    categories = [category.name.capitalize() for category in categories]
    return JsonResponse({'categories': categories})


def clear_localstorage(request):
    ''' GET METHOD TO TELL FRONTEND TEMPLATE TO CLEAN THE CART '''

    if request.session.get('clear_localstorage'):
        request.session['clear_localstorage'] = False
        return JsonResponse({'clear_localstorage': True})

    return JsonResponse({'clear_localstorage': False})
