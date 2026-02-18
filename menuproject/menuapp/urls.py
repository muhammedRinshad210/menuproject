from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:id>/', views.edit_carousel, name='edit_carousel'),
    path('delete/<int:id>/', views.delete_carousel, name='delete_carousel'),
    path('juices/', views.juices,name='juices'),
    path('chai/', views.chai,name='chai'),
    path('fastfood', views.fastfood, name = 'fastfood'),
    path('add-cart/<int:id>/', views.add_to_cart, name='add_cart'),
    path('cart/', views.cart_page, name='cart'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/delete/<int:id>/', views.delete_product, name='delete_product'),

]
