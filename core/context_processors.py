from django.conf import settings
from django.core.cache import cache

from cart.services import get_user_cart_items_count
from catalog.models import Category


def shop_context(request):
    categories = cache.get('active_categories')
    if categories is None:
        categories = list(Category.objects.filter(is_active=True).only('name', 'slug'))
        cache.set('active_categories', categories, 60)

    cart_items_count = get_user_cart_items_count(request.user)
    is_manager_or_admin = request.user.is_authenticated and (
        request.user.is_superuser or request.user.groups.filter(name='Manager').exists()
    )

    return {
        'SHOP_NAME': settings.SHOP_NAME,
        'SUPPORT_EMAIL': settings.SUPPORT_EMAIL,
        'shop_categories': categories,
        'cart_items_count': cart_items_count,
        'is_manager_or_admin': is_manager_or_admin,
        'view_mode': request.COOKIES.get('view_mode', 'grid'),
        'banner_closed': request.COOKIES.get('banner_closed') == '1',
    }
