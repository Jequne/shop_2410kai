from django.urls import path

from managerpanel.views import manager_orders_view, update_order_status_view

app_name = 'managerpanel'

urlpatterns = [
    path('orders/', manager_orders_view, name='orders'),
    path('orders/<int:order_id>/status/', update_order_status_view, name='update_status'),
]
