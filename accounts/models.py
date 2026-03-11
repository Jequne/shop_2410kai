from django.conf import settings
from django.db import models


class Profile(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
	phone = models.CharField('Телефон', max_length=32, blank=True)
	address = models.CharField('Адрес', max_length=255, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

	def __str__(self) -> str:
		return f'Профиль: {self.user.username}'

# Create your models here.
