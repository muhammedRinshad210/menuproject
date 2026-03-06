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
    offer = Offer.objects.filter(is_active=True).first()

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_count = Cart.objects.filter(session_key=session_key).count() + \
             SpecialCart.objects.filter(session_key=session_key).count()

    return render(request, 'menuapp/index.html', {
        'carousels': carousels,
        'special_items': special_items,
        'cart_count': cart_count,
        'offer': offer,   # 🔥 IMPORTANT
    })


from django.shortcuts import render, redirect
from .models import Carousel, MenuItem, SpecialItem, ChatMessage
from .forms import CarouselForm, MenuItemForm, SpecialItemForm


from .models import Offer
from .forms import OfferForm

def dashboard(request):

    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')
    messages = ChatMessage.objects.all().order_by('-id')
    offers = Offer.objects.all().order_by('-id')

    carousel_form = CarouselForm()
    product_form = MenuItemForm()
    special_form = SpecialItemForm()
    offer_form = OfferForm()

    if request.method == "POST":

        if "offer_submit" in request.POST:
            offer_form = OfferForm(request.POST)
            if offer_form.is_valid():
                Offer.objects.update(is_active=False)
                offer_form.save()
                return redirect("dashboard")

        elif "carousel_submit" in request.POST:
            carousel_form = CarouselForm(request.POST, request.FILES)
            if carousel_form.is_valid():
                carousel_form.save()
                return redirect("dashboard")

        elif "product_submit" in request.POST:
            product_form = MenuItemForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return redirect("dashboard")

        elif "special_submit" in request.POST:
            special_form = SpecialItemForm(request.POST, request.FILES)
            if special_form.is_valid():
                special_form.save()
                return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "carousel_form": carousel_form,
        "product_form": product_form,
        "special_form": special_form,
        "offer_form": offer_form,
        "carousels": carousels,
        "products": products,
        "special_items": special_items,
        "messages": messages,
        "offers": offers,
    })


# Edit Carousel
from django.shortcuts import get_object_or_404, redirect, render

def edit_carousel(request, id):
    carousel = get_object_or_404(Carousel, id=id)

    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')
    messages = ChatMessage.objects.all().order_by('-id')

    carousel_form = CarouselForm(instance=carousel)
    product_form = MenuItemForm()
    special_form = SpecialItemForm()

    if request.method == "POST":
        carousel_form = CarouselForm(request.POST, request.FILES, instance=carousel)
        if carousel_form.is_valid():
            carousel_form.save()
            return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "carousel_form": carousel_form,   # IMPORTANT
        "product_form": product_form,
        "special_form": special_form,
        "carousels": carousels,
        "products": products,
        "special_items": special_items,
        "messages": messages,
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

        

    return redirect('cart')


from .models import SpecialItem, SpecialCart
from django.db import transaction


def add_special_to_cart(request, item_id):

    item = get_object_or_404(SpecialItem, id=item_id)

    try:
        requested_qty = int(request.POST.get('quantity', 1))
    except ValueError:
        requested_qty = 1

    if requested_qty <= 0:
        return redirect('cart')

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    if item.quantity <= 0:
        return redirect('cart')

    if requested_qty > item.quantity:
        requested_qty = item.quantity

    cart_item = SpecialCart.objects.filter(
        item=item,
        session_key=session_key
    ).first()

    if cart_item:
        cart_item.quantity += requested_qty
        cart_item.save()
    else:
        SpecialCart.objects.create(
            item=item,
            quantity=requested_qty,
            session_key=session_key
        )

    return redirect('cart')




def increase_special_cart(request, cart_id):

    cart = get_object_or_404(SpecialCart, id=cart_id)
    product = cart.item

    max_allowed = product.quantity

    if cart.quantity < max_allowed:
        cart.quantity += 1
        cart.save()

    return redirect('cart')


def decrease_special_cart(request, cart_id):
    cart = get_object_or_404(SpecialCart, id=cart_id)

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return redirect('cart')




def remove_special_cart(request, cart_id):
    cart = get_object_or_404(SpecialCart, id=cart_id)
    cart.delete()
    return redirect('cart')



# Cart page
def cart_page(request):
    session_key = request.session.session_key
    cart_items = Cart.objects.filter(session_key=session_key)
    special_cart_items = SpecialCart.objects.filter(session_key=session_key)
    
    total = sum(i.total_price() for i in cart_items) + \
            sum(i.total_price() for i in special_cart_items)

    return render(request, "menuapp/cart.html", {
        "cart_items": cart_items,
        "special_cart_items": special_cart_items,
        "total": total
    })



from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart


def increase_cart(request, cart_id):

    cart = get_object_or_404(Cart, id=cart_id)
    product = cart.item

    # calculate max allowed
    max_allowed = product.quantity

    if cart.quantity < max_allowed:
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


from django.db import transaction

def checkout(request):

    session_key = request.session.session_key

    cart_items = Cart.objects.filter(session_key=session_key)
    special_items = SpecialCart.objects.filter(session_key=session_key)

    with transaction.atomic():

        # Reduce stock for normal items
        for cart in cart_items:
            item = cart.item

            if item.quantity >= cart.quantity:
                item.quantity -= cart.quantity
                item.save()

        # Reduce stock for special items
        for cart in special_items:
            item = cart.item

            if item.quantity >= cart.quantity:
                item.quantity -= cart.quantity
                item.save()

        # Clear cart
        cart_items.delete()
        special_items.delete()

    return render(request, "menuapp/checkout.html")


def edit_special(request, id):
    item = get_object_or_404(SpecialItem, id=id)

    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')
    messages = ChatMessage.objects.all().order_by('-id')

    special_form = SpecialItemForm(instance=item)
    carousel_form = CarouselForm()
    product_form = MenuItemForm()

    if request.method == "POST":
        special_form = SpecialItemForm(request.POST, request.FILES, instance=item)
        if special_form.is_valid():
            special_form.save()
            return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "carousel_form": carousel_form,
        "product_form": product_form,
        "special_form": special_form,
        "carousels": carousels,
        "products": products,
        "special_items": special_items,
        "messages": messages,
    })


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


from .models import ChatMessage
from django.shortcuts import render, redirect




def chat_page(request):
    if request.method == "POST":
        name = request.POST.get('name')
        message = request.POST.get('message')
        rating = request.POST.get('rating')

        if not rating:
            rating = 0

        ChatMessage.objects.create(
            name=name,
            message=message,
            rating=int(rating)   # ⭐ VERY IMPORTANT
        )

        return redirect('chat')

    return render(request, 'menuapp/chat.html')






def contact_page(request):
    return render(request, "menuapp/contact.html")



# qr section : 

from django.shortcuts import render, redirect, get_object_or_404
from .models import Table
from django.contrib import messages

# Dashboard Table List
def dashboard_tables(request):
    tables = Table.objects.all().order_by('table_number')
    return render(request, "menuapp/admin/tables.html", {"tables": tables})


# Toggle Active/Inactive
def toggle_table(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table.is_active = not table.is_active
    table.save()
    return redirect("dashboard_tables")


# Create Tables Automatically (1–20)
def create_tables(request):
    for i in range(1, 11):
        Table.objects.get_or_create(table_number=i)
    return redirect("dashboard_tables")


def table_view(request, table_number):
    try:
        table = Table.objects.get(table_number=table_number)

        if not table.is_active:
            return render(request, "menuapp/table_disabled.html")

        request.session['table_number'] = table_number
        return redirect("home")

    except Table.DoesNotExist:
        return render(request, "menuapp/table_disabled.html")
    

from django.shortcuts import get_object_or_404, redirect

def delete_table(request, pk):
    table = get_object_or_404(Table, pk=pk)
    table.delete()
    return redirect("dashboard_tables")



# offer 



from django.shortcuts import redirect, get_object_or_404
from .models import Offer

def delete_offer(request, id):
    offer = get_object_or_404(Offer, id=id)
    offer.delete()
    return redirect('dashboard')



def edit_offer(request, id):
    offer = get_object_or_404(Offer, id=id)

    carousels = Carousel.objects.all().order_by('-id')
    products = MenuItem.objects.all().order_by('-id')
    special_items = SpecialItem.objects.all().order_by('-id')
    messages = ChatMessage.objects.all().order_by('-id')
    offers = Offer.objects.all().order_by('-id')

    offer_form = OfferForm(instance=offer)
    carousel_form = CarouselForm()
    product_form = MenuItemForm()
    special_form = SpecialItemForm()

    if request.method == "POST":
        offer_form = OfferForm(request.POST, instance=offer)
        if offer_form.is_valid():
            Offer.objects.update(is_active=False)
            offer_form.save()
            return redirect("dashboard")

    return render(request, "menuapp/admin/dashboard.html", {
        "carousel_form": carousel_form,
        "product_form": product_form,
        "special_form": special_form,
        "offer_form": offer_form,
        "carousels": carousels,
        "products": products,
        "special_items": special_items,
        "messages": messages,
        "offers": offers,
    })