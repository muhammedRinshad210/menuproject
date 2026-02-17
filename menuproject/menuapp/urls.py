from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:id>/', views.edit_carousel, name='edit_carousel'),
    path('delete/<int:id>/', views.delete_carousel, name='delete_carousel'),

    # juice urls
    path('juices/', views.juices,name='juices'),


    # chai urls
    path('chai/', views.chai,name='chai'),


    # fastfood urls 
    path('fastfood', views.fastfood, name = 'fastfood'),
]
