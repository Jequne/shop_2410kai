from django.urls import path

from orders.views import checkout_view, delete_receipt_view, order_detail_view

app_name = 'orders'

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('orders/<int:order_id>/', order_detail_view, name='order_detail'),
    path('orders/<int:order_id>/delete-receipt/', delete_receipt_view, name='delete_receipt'),
]
