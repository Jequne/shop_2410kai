from datetime import timedelta

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone


class Order(models.Model):
	class Status(models.TextChoices):
		NEW = 'NEW', 'Новый'
		PAID_MOCK = 'PAID_MOCK', 'Оплачен (муляж)'
		PROCESSING = 'PROCESSING', 'В обработке'
		SHIPPED = 'SHIPPED', 'Отправлен'
		DELIVERED = 'DELIVERED', 'Доставлен'
		CANCELED = 'CANCELED', 'Отменен'

	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
	total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'
		ordering = ['-created_at']

	def __str__(self) -> str:
		return f'Заказ #{self.pk}'

	def recalc_total(self):
		self.total_price = sum(item.price_at_purchase * item.quantity for item in self.items.all())
		self.save(update_fields=['total_price', 'updated_at'])


class OrderItem(models.Model):
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
	product = models.ForeignKey('catalog.Product', on_delete=models.PROTECT, related_name='order_items')
	price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

	class Meta:
		verbose_name = 'Позиция заказа'
		verbose_name_plural = 'Позиции заказа'

	def __str__(self) -> str:
		return f'{self.product.name} x {self.quantity}'


class Receipt(models.Model):
	order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='receipt')
	content = models.TextField('Содержимое чека', blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	deleted_at = models.DateTimeField(null=True, blank=True)

	class Meta:
		verbose_name = 'Чек'
		verbose_name_plural = 'Чеки'

	def __str__(self) -> str:
		return f'Чек к заказу #{self.order_id}'

	@property
	def can_be_deleted_by_user(self) -> bool:
		return timezone.now() >= self.created_at + timedelta(days=5)

# Create your models here.
