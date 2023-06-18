"""distutils.command.bdist_dumb

Implements the Distutils 'bdist_dumb' command (create a "dumb" built
distribution -- i.e., just an archive to be unpacked under $prefix or
$exec_prefix)."""

import os
from django.contrib import admin
from django.urls import path
from .import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HOME, name = 'home'),
    path('base/', views.BASE, name='base'),
    path('products/',views.PRODUCT, name = 'products'),
    path('search/',views.SEARCH, name = 'search'),
    path('products/<str:id>',views.PRODUCT_DETAILS,name = 'product_details'),
    path('contact/',views.CONTACT_US, name='contact'),
    path('register/',views.HandleRegister, name = 'register'),
    path('login/',views.HandleLogin, name = 'login'),
    path('logout/',views.HandleLogout, name = 'logout'),
    path('about/',views.about, name = 'about'),
    #path('cart/cart_detail/',views.CART, name = 'cart_detail'),
    path('profileview/',views.profileview, name = 'profileview'),


    #CART
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
       views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
       views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('cart/checkout/',views.CHECK_OUT,name='checkout'),
    path('cart/checkout/placeorder',views.PLACE_ORDER, name='place_order'),
    path('success/',views.SUCCESS,name='success'),

    ] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)