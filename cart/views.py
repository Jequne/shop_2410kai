from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from cart.forms import CartItemUpdateForm
from cart.models import CartItem
from cart.services import get_or_create_cart
from catalog.models import Product


def _build_cart_header_context(user):
	cart = get_or_create_cart(user)
	all_items = list(cart.items.select_related('product'))
	return {
		'cart_items_count': sum(item.quantity for item in all_items),
		'cart_preview_items': all_items[:3],
		'cart_preview_total': sum(item.line_total for item in all_items),
	}


def _render_cart_header_state(request, user):
	context = _build_cart_header_context(user)
	return render(request, 'cart/partials/cart_header_state.html', context)


@login_required
def cart_detail_view(request: HttpRequest) -> HttpResponse:
	cart = get_or_create_cart(request.user)
	items = cart.items.select_related('product').all()
	return render(request, 'cart/cart_detail.html', {'cart': cart, 'items': items})


@login_required
def add_to_cart_view(request: HttpRequest, slug: str) -> HttpResponse:
	if request.method != 'POST':
		return redirect('catalog:product_detail', slug=slug)

	product = get_object_or_404(Product, slug=slug, is_active=True)
	cart = get_or_create_cart(request.user)
	item, created = CartItem.objects.get_or_create(cart=cart, product=product)
	if not created:
		item.quantity = F('quantity') + 1
		item.save(update_fields=['quantity'])
		item.refresh_from_db()

	if request.htmx:
		return _render_cart_header_state(request, request.user)

	messages.success(request, f'Товар «{product.name}» добавлен в корзину.')
	return redirect('catalog:product_detail', slug=slug)


@login_required
def update_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
	item = get_object_or_404(CartItem.objects.select_related('cart', 'product'), id=item_id, cart__user=request.user)

	form = CartItemUpdateForm(request.POST)
	if form.is_valid():
		item.quantity = form.cleaned_data['quantity']
		item.save(update_fields=['quantity'])

	if request.htmx:
		return render(request, 'cart/partials/cart_items_table.html', {'cart': item.cart, 'items': item.cart.items.select_related('product').all()})

	return redirect('cart:detail')


@login_required
def remove_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
	item = get_object_or_404(CartItem.objects.select_related('cart'), id=item_id, cart__user=request.user)
	cart = item.cart
	item.delete()

	if request.htmx:
		return render(request, 'cart/partials/cart_items_table.html', {'cart': cart, 'items': cart.items.select_related('product').all()})

	return redirect('cart:detail')


@login_required
def increase_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
	if request.method != 'POST':
		return redirect('cart:detail')

	item = get_object_or_404(CartItem.objects.select_related('cart', 'product'), id=item_id, cart__user=request.user)
	item.quantity = F('quantity') + 1
	item.save(update_fields=['quantity'])

	if request.htmx:
		return _render_cart_header_state(request, request.user)

	return redirect('cart:detail')


@login_required
def decrease_cart_item_view(request: HttpRequest, item_id: int) -> HttpResponse:
	if request.method != 'POST':
		return redirect('cart:detail')

	item = get_object_or_404(CartItem.objects.select_related('cart', 'product'), id=item_id, cart__user=request.user)
	if item.quantity <= 1:
		item.delete()
	else:
		item.quantity = F('quantity') - 1
		item.save(update_fields=['quantity'])

	if request.htmx:
		return _render_cart_header_state(request, request.user)

	return redirect('cart:detail')

# Create your views here.
