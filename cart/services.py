from cart.models import Cart


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def get_user_cart_items_count(user):
    if not user.is_authenticated:
        return 0
    cart = getattr(user, 'cart', None)
    if not cart:
        return 0
    return sum(item.quantity for item in cart.items.all())
