from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "menuapp/index.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Carousel
from .forms import CarouselForm


# Home Page
def home(request):
    carousels = Carousel.objects.all().order_by('-id')
    return render(request, 'menuapp/index.html', {'carousels': carousels})


# Dashboard Page
def dashboard(request):
    carousels = Carousel.objects.all().order_by('-id')
    form = CarouselForm()

    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(request, 'menuapp/admin/dashboard.html', {
        'form': form,
        'carousels': carousels
    })


# Edit Carousel
def edit_carousel(request, id):
    carousel = get_object_or_404(Carousel, id=id)
    form = CarouselForm(instance=carousel)

    if request.method == 'POST':
        form = CarouselForm(request.POST, request.FILES, instance=carousel)
        if form.is_valid():
            form.save()
            return redirect('dashboard')

    return render(request, 'menuapp/admin/dashboard.html', {
        'form': form,
        'carousels': Carousel.objects.all()
    })


# Delete Carousel
def delete_carousel(request, id):
    carousel = get_object_or_404(Carousel, id=id)
    carousel.delete()
    return redirect('dashboard')
