from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('product/', views.product, name="product"),
    path('product_detail/<str:pk>', views.product_detail, name='product_detail'),
    path('order', views.order, name='order'),
    path('order_detail/<str:stripe_id>',
         views.order_detail, name='order_detail'),
    path('cart_detail/', views.cart_detail, name="cart_detail"),
    path('checkout_redirect/', views.checkout_redirect, name='checkout_redirect'),
    path('checkout', views.checkout, name='checkout'),
    path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('get_categories/', views.get_categories, name='get_categories'),
    path('clear_localstorage/', views.clear_localstorage,
         name="clear_localstorage"),
]
