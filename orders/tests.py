from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from cart.models import CartItem
from cart.services import get_or_create_cart
from catalog.models import Category, Product
from orders.models import Order, OrderItem, Receipt


class CheckoutFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username='checkout-user',
			email='checkout@example.com',
			password='StrongPass123!',
		)
		self.client.force_login(self.user)

		category = Category.objects.create(name='Электроника', slug='electronics', is_active=True)
		self.product = Product.objects.create(
			category=category,
			name='Портативная колонка',
			slug='portable-speaker',
			description='Колонка с Bluetooth',
			price=Decimal('4590.00'),
			stock_quantity=20,
			is_active=True,
		)

	def test_checkout_creates_order_and_receipt_and_clears_cart(self):
		add_response = self.client.post(reverse('cart:add', kwargs={'slug': self.product.slug}))
		self.assertEqual(add_response.status_code, 302)

		checkout_response = self.client.post(reverse('orders:checkout'), {'payment_method': 'card_mock'})
		self.assertEqual(checkout_response.status_code, 302)

		order = Order.objects.filter(user=self.user).order_by('-id').first()
		self.assertIsNotNone(order)
		self.assertEqual(order.status, Order.Status.PAID_MOCK)
		self.assertEqual(order.items.count(), 1)

		receipt = Receipt.objects.filter(order=order).first()
		self.assertIsNotNone(receipt)

		cart = get_or_create_cart(self.user)
		self.assertEqual(CartItem.objects.filter(cart=cart).count(), 0)

	def test_order_detail_renders_with_receipt(self):
		order = Order.objects.create(user=self.user, status=Order.Status.PAID_MOCK)
		OrderItem.objects.create(
			order=order,
			product=self.product,
			price_at_purchase=self.product.price,
			quantity=1,
		)
		order.recalc_total()
		Receipt.objects.create(order=order, content='Чек тестовый')

		response = self.client.get(reverse('orders:order_detail', kwargs={'order_id': order.id}))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Чек тестовый')
