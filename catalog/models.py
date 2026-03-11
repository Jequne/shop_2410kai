from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg


class Category(models.Model):
	name = models.CharField('Название', max_length=120)
	slug = models.SlugField('Slug', unique=True)
	is_active = models.BooleanField('Активна', default=True)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class Product(models.Model):
	category = models.ForeignKey(
		Category,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='products',
		verbose_name='Категория',
	)
	name = models.CharField('Название', max_length=150)
	slug = models.SlugField('Slug', unique=True)
	description = models.TextField('Описание')
	price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
	image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
	stock_quantity = models.PositiveIntegerField('Остаток', default=0)
	is_active = models.BooleanField('Активен', default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
		ordering = ['-created_at']

	def __str__(self) -> str:
		return self.name

	@property
	def average_rating(self) -> float:
		value = self.reviews.aggregate(avg=Avg('rating'))['avg']
		return round(value or 0, 2)


class ProductImage(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery_images', verbose_name='Товар')
	image = models.ImageField('Изображение', upload_to='products/gallery/')
	alt_text = models.CharField('Alt-текст', max_length=150, blank=True)
	position = models.PositiveSmallIntegerField('Позиция', default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Дополнительное изображение товара'
		verbose_name_plural = 'Дополнительные изображения товаров'
		ordering = ['position', 'id']

	def __str__(self) -> str:
		return f'Изображение для {self.product.name}'


class ProductReview(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name='Товар')
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name='Автор')
	text = models.TextField('Отзыв')
	rating = models.PositiveSmallIntegerField(
		'Оценка',
		validators=[MinValueValidator(1), MaxValueValidator(5)],
	)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = 'Отзыв'
		verbose_name_plural = 'Отзывы'
		ordering = ['-created_at']
		constraints = [
			models.UniqueConstraint(fields=['product', 'author'], name='unique_review_per_product_author')
		]

	def __str__(self) -> str:
		return f'Отзыв {self.author} на {self.product}'

# Create your models here.
