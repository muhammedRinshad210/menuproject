from .models import Cart

def cart_data(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart_items = Cart.objects.filter(session_key=session_key)
    count = cart_items.count()

    return {
        "cart_items": cart_items,
        "cart_count": count
    }