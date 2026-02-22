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


from django.shortcuts import render, redirect
from .models import Carousel, MenuItem, SpecialItem
from .forms import CarouselForm, MenuItemForm, SpecialItemForm


def dashboard(request):

    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')

    # Default empty forms
    carousel_form = CarouselForm()
    product_form = MenuItemForm()
    special_form = SpecialItemForm()

    if request.method == "POST":

        # ---- Carousel submit ----
        if "carousel_submit" in request.POST:
            carousel_form = CarouselForm(request.POST, request.FILES)
            if carousel_form.is_valid():
                carousel_form.save()
                return redirect("dashboard")

        # ---- Product submit ----
        elif "product_submit" in request.POST:
            product_form = MenuItemForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return redirect("dashboard")

        # ---- Special Item submit ----
        elif "special_submit" in request.POST:
            special_form = SpecialItemForm(request.POST, request.FILES)
            if special_form.is_valid():
                special_form.save()
                return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "carousel_form": carousel_form,   # ✅ fixed key name
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

from django.shortcuts import get_object_or_404, redirect
from django.db import transaction

def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    # Get quantity from form (default 1)
    try:
        requested_qty = int(request.POST.get('quantity', 1))
    except ValueError:
        requested_qty = 1

    # Prevent negative or zero quantity
    if requested_qty <= 0:
        return redirect('cart')

    # Ensure session exists
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    # If no stock available
    if item.quantity <= 0:
        return redirect('cart')

    # Do not allow more than available stock
    if requested_qty > item.quantity:
        requested_qty = item.quantity

    with transaction.atomic():

        cart_item = Cart.objects.filter(
            item=item,
            session_key=session_key
        ).first()

        if cart_item:
            cart_item.quantity += requested_qty
            cart_item.save()
        else:
            cart_item = Cart.objects.create(
                item=item,
                quantity=requested_qty,
                session_key=session_key
            )

        # Reduce stock
        item.quantity -= requested_qty
        item.save()

    return redirect('cart')


# Cart page
def cart_page(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)
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


from .models import Cart

def cart_count(request):
    session_key = request.session.session_key

    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    count = Cart.objects.filter(session_key=session_key).count()

    return {
        'cart_count': count
    }