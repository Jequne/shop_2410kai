from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Cart(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Корзина'
		verbose_name_plural = 'Корзины'

	def __str__(self) -> str:
		return f'Корзина: {self.user.username}'

	@property
	def total_price(self):
		return sum(item.line_total for item in self.items.select_related('product'))


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='cart_items')
	quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)], default=1)

	class Meta:
		verbose_name = 'Позиция корзины'
		verbose_name_plural = 'Позиции корзины'
		constraints = [
			models.UniqueConstraint(fields=['cart', 'product'], name='unique_cart_product')
		]

	@property
	def line_total(self):
		return self.product.price * self.quantity

	def __str__(self) -> str:
		return f'{self.product.name} x {self.quantity}'

# Create your models here.
