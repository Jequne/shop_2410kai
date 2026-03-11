from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from cart.services import get_or_create_cart
from orders.forms import CheckoutForm
from orders.models import Order, OrderItem, Receipt


@login_required
def checkout_view(request: HttpRequest) -> HttpResponse:
	cart = get_or_create_cart(request.user)
	items = cart.items.select_related('product').all()

	if not items:
		messages.warning(request, 'Корзина пуста. Добавьте товары перед оформлением заказа.')
		return redirect('cart:detail')

	if request.method == 'POST':
		form = CheckoutForm(request.POST)
		if form.is_valid():
			payment_method = form.cleaned_data['payment_method']
			request.session['checkout_last_payment_method'] = payment_method

			order = Order.objects.create(user=request.user, status=Order.Status.PAID_MOCK)
			order_items = []
			for item in items:
				order_items.append(
					OrderItem(
						order=order,
						product=item.product,
						price_at_purchase=item.product.price,
						quantity=item.quantity,
					)
				)
			OrderItem.objects.bulk_create(order_items)
			order.recalc_total()

			receipt_text = (
				f'Чек по заказу #{order.id}\\n'
				f'Пользователь: {request.user.username}\\n'
				f'Дата: {timezone.localtime(order.created_at).strftime("%d.%m.%Y %H:%M")}\\n'
				f'Сумма: {order.total_price} руб.\\n'
				f'Способ оплаты: {payment_method}'
			)
			Receipt.objects.create(order=order, content=receipt_text)

			items.delete()
			messages.success(request, f'Заказ #{order.id} успешно оформлен.')
			return redirect('orders:order_detail', order_id=order.id)
	else:
		initial_payment = request.session.get('checkout_last_payment_method', 'card_mock')
		form = CheckoutForm(initial={'payment_method': initial_payment})

	return render(request, 'orders/checkout.html', {'cart': cart, 'items': items, 'form': form})


@login_required
def order_detail_view(request: HttpRequest, order_id: int) -> HttpResponse:
	order = get_object_or_404(
		Order.objects.select_related('receipt').prefetch_related('items__product'),
		id=order_id,
		user=request.user,
	)
	return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def delete_receipt_view(request: HttpRequest, order_id: int) -> HttpResponse:
	if request.method != 'POST':
		return redirect('orders:order_detail', order_id=order_id)

	order = get_object_or_404(Order.objects.select_related('receipt'), id=order_id, user=request.user)
	receipt = getattr(order, 'receipt', None)
	if not receipt:
		messages.warning(request, 'Чек уже отсутствует.')
		return redirect('orders:order_detail', order_id=order_id)

	if not receipt.can_be_deleted_by_user:
		messages.error(request, 'Удаление чека возможно только через 5 дней после его создания.')
		return redirect('orders:order_detail', order_id=order_id)

	receipt.deleted_at = timezone.now()
	receipt.content = ''
	receipt.save(update_fields=['deleted_at', 'content'])
	messages.success(request, 'Чек удален.')
	return redirect('orders:order_detail', order_id=order_id)

# Create your views here.
