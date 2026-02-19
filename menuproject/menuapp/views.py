from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "menuapp/index.html")

from django.shortcuts import render, redirect, get_object_or_404
from .models import Carousel
from .forms import CarouselForm


# Home Page
from .models import Carousel, SpecialItem

from .models import Cart

def home(request):
    carousels = Carousel.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')

    cart_count = Cart.objects.count()

    return render(request, 'menuapp/index.html', {
        'carousels': carousels,
        'special_items': special_items,
        'cart_count': cart_count
    })



from .models import Carousel, MenuItem, SpecialItem
from .forms import CarouselForm, MenuItemForm, SpecialItemForm
from django.shortcuts import render, redirect, get_object_or_404


def dashboard(request):
    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')

    carousel_form = CarouselForm()
    product_form = MenuItemForm()
    special_form = SpecialItemForm()

    # ---- Carousel submit ----
    if request.method == "POST" and "carousel_submit" in request.POST:
        carousel_form = CarouselForm(request.POST, request.FILES)
        if carousel_form.is_valid():
            carousel_form.save()
            return redirect("dashboard")

    # ---- Product submit ----
    if request.method == "POST" and "product_submit" in request.POST:
        product_form = MenuItemForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return redirect("dashboard")

    # ---- Special Item submit ----
    if request.method == "POST" and "special_submit" in request.POST:
        special_form = SpecialItemForm(request.POST, request.FILES)
        if special_form.is_valid():
            special_form.save()
            return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "form": carousel_form,
        "product_form": product_form,
        "special_form": special_form,
        "carousels": carousels,
        "products": products,
        "special_items": special_items
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

from .models import MenuItem, Cart
from django.shortcuts import redirect

def juices(request):
    items = MenuItem.objects.filter(category="juice")
    return render(request, "menuapp/juices.html", {"items": items})

def chai(request):
    items = MenuItem.objects.filter(category="chai")
    return render(request, "menuapp/chai.html", {"items": items})

def fastfood(request):
    items = MenuItem.objects.filter(category="fastfood")
    return render(request, "menuapp/fastfood.html", {"items": items})



def edit_product(request, id):
    product = get_object_or_404(MenuItem, id=id)
    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')

    product_form = MenuItemForm(instance=product)
    carousel_form = CarouselForm()

    if request.method == "POST":
        product_form = MenuItemForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "form": carousel_form,
        "product_form": product_form,
        "carousels": carousels,
        "products": products
    })



def delete_product(request, id):
    product = get_object_or_404(MenuItem, id=id)
    product.delete()
    return redirect("dashboard")






from django.shortcuts import get_object_or_404, redirect

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    if item.quantity <= 0:
        return redirect('cart')

    cart_item = Cart.objects.filter(item=item).first()

    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = Cart.objects.create(item=item, quantity=1)

    cart_item.save()

    # decrease stock
    item.quantity -= 1
    item.save()

    return redirect('cart')





# Cart page
def cart_page(request):
    cart_items = Cart.objects.all()
    total = sum(i.total_price() for i in cart_items)

    return render(request, "menuapp/cart.html", {
        "cart_items": cart_items,
        "total": total
    })
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart


def increase_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.quantity += 1
    cart.save()
    return redirect('cart')


def decrease_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return redirect('cart')


def remove_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    cart.delete()
    return redirect('cart')


def checkout(request):
    return render(request, 'menuapp/checkout.html')


def edit_special(request, id):
    item = SpecialItem.objects.get(id=id)
    form = SpecialItemForm(request.POST or None, request.FILES or None, instance=item)
    if form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'dashboard.html', {'special_form': form})


def delete_special(request, id):
    item = SpecialItem.objects.get(id=id)
    item.delete()
    return redirect('dashboard')
