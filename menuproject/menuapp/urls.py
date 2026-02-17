from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<int:id>/', views.edit_carousel, name='edit_carousel'),
    path('delete/<int:id>/', views.delete_carousel, name='delete_carousel'),
]
