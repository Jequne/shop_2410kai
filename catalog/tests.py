from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product


class CatalogSmokeTests(TestCase):
	def setUp(self):
		category = Category.objects.create(name='Тестовая категория', slug='test-category', is_active=True)
		Product.objects.create(
			category=category,
			name='Тестовый товар',
			slug='test-product',
			description='Описание',
			price=Decimal('1990.00'),
			stock_quantity=10,
			is_active=True,
		)

	def test_product_list_page_renders(self):
		response = self.client.get(reverse('catalog:product_list'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Каталог товаров')
