from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('product/', views.product, name="product"),
    path('product_detail/<str:pk>', views.product_detail, name='product_detail'),
    path('cart_detail/', views.cart_detail, name="cart_detail"),
    path('checkout/', views.checkout, name='checkout'),
]
