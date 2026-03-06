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

    
    path('chat/', views.chat_page, name='chat'),

    path('contact',views.contact_page, name='contact'),

          
    path("dashboard/tables/", views.dashboard_tables, name="dashboard_tables"),
    path("dashboard/tables/delete/<int:pk>/", views.delete_table, name="delete_table"),
    path("dashboard/tables/toggle/<int:pk>/", views.toggle_table, name="toggle_table"),
    path("dashboard/tables/create/", views.create_tables, name="create_tables"),
    path("table/<int:table_number>/", views.table_view, name="table_view"),

    # offer  
    path('delete-offer/<int:id>/', views.delete_offer, name='delete_offer'),
    path('edit-offer/<int:id>/', views.edit_offer, name='edit_offer'),
    path('add-special-to-cart/<int:item_id>/', views.add_special_to_cart, name='add_special_to_cart'),
    path('increase-special/<int:cart_id>/', views.increase_special_cart, name='increase_special_cart'),
    path('decrease-special/<int:cart_id>/', views.decrease_special_cart, name='decrease_special_cart'),
    path('remove-special/<int:cart_id>/', views.remove_special_cart, name='remove_special_cart'),
    path("admin-bill/<int:order_id>/", views.admin_bill, name="admin_bill"),
    

]
