from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Carousel
    path('edit/<int:id>/', views.edit_carousel, name='edit_carousel'),
    path('delete/<int:id>/', views.delete_carousel, name='delete_carousel'),

    # Products
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('delete-product/<int:id>/', views.delete_product, name='delete_product'),

    # Menu categories
    path('juices/', views.juices, name='juices'),
    path('chai/', views.chai, name='chai'),
    path('fastfood/', views.fastfood, name='fastfood'),

    # Cart
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart'),

    path('increase-cart/<int:cart_id>/', views.increase_cart, name='increase_cart'),
    path('decrease-cart/<int:cart_id>/', views.decrease_cart, name='decrease_cart'),
    path('remove-cart/<int:cart_id>/', views.remove_cart, name='remove_cart'),

    path('checkout/', views.checkout, name='checkout'),
    path('edit-special/<int:id>/', views.edit_special, name='edit_special'),
    path('delete-special/<int:id>/', views.delete_special, name='delete_special'),

]
