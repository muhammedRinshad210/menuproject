from menuproject.menuapp.models import Cart

def cart_data(request):
    cart_items = Cart.objects.all()
    return {'cart_items': cart_items}

def cart_count(request):
    count = Cart.objects.count()
    return {"cart_count": count}

