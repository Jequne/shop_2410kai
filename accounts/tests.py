from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountAuthFlowTests(TestCase):
	def test_signup_requires_only_email_and_passwords(self):
		response = self.client.post(
			reverse('accounts:signup'),
			{
				'email': 'newuser@example.com',
				'password1': 'StrongPass123!',
				'password2': 'StrongPass123!',
			},
		)

		self.assertRedirects(response, reverse('catalog:product_list'), fetch_redirect_response=False)
		user = User.objects.get(email='newuser@example.com')
		self.assertTrue(user.username)
		self.assertNotEqual(user.username, '')
		self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

	def test_login_uses_email_instead_of_username(self):
		user = User.objects.create_user(
			username='stored-username',
			email='customer@example.com',
			password='StrongPass123!',
		)

		response = self.client.post(
			reverse('accounts:login'),
			{
				'email': 'customer@example.com',
				'password': 'StrongPass123!',
			},
		)

		self.assertRedirects(response, reverse('catalog:product_list'), fetch_redirect_response=False)
		self.assertEqual(int(self.client.session['_auth_user_id']), user.id)

	def test_logout_endpoint_logs_user_out_via_post(self):
		user = User.objects.create_user(
			username='logout-user',
			email='logout@example.com',
			password='StrongPass123!',
		)
		self.client.force_login(user)

		response = self.client.post(reverse('accounts:logout'))

		self.assertRedirects(response, reverse('core:landing'), fetch_redirect_response=False)
		self.assertNotIn('_auth_user_id', self.client.session)
