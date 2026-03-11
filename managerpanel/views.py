from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from orders.forms import OrderStatusForm
from orders.models import Order


def _is_manager_or_admin(user):
	return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Manager').exists())


@login_required
@user_passes_test(_is_manager_or_admin)
def manager_orders_view(request: HttpRequest) -> HttpResponse:
	orders = Order.objects.select_related('user').all()
	return render(request, 'managerpanel/orders.html', {'orders': orders, 'status_choices': Order.Status.choices})


@login_required
@user_passes_test(_is_manager_or_admin)
def update_order_status_view(request: HttpRequest, order_id: int) -> HttpResponse:
	order = get_object_or_404(Order, id=order_id)
	form = OrderStatusForm(request.POST, instance=order)
	if form.is_valid():
		form.save()

	if request.htmx:
		return render(request, 'managerpanel/partials/order_status_cell.html', {'order': order, 'status_choices': Order.Status.choices})

	return redirect('managerpanel:orders')

# Create your views here.
