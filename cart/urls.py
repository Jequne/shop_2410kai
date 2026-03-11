from django.urls import path

from cart.views import add_to_cart_view, cart_detail_view, remove_cart_item_view, update_cart_item_view

app_name = 'cart'

urlpatterns = [
    path('', cart_detail_view, name='detail'),
    path('add/<slug:slug>/', add_to_cart_view, name='add'),
    path('item/<int:item_id>/update/', update_cart_item_view, name='update_item'),
    path('item/<int:item_id>/remove/', remove_cart_item_view, name='remove_item'),
]
