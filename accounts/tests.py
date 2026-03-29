from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AccountFlowTests(TestCase):
	def setUp(self):
		self.password = 'StrongPassword123!'
		self.user = get_user_model().objects.create_user(
			email='existing@example.com',
			password=self.password,
			first_name='Existing',
			last_name='User',
		)

	def test_signup_creates_user_and_logs_in(self):
		response = self.client.post(
			reverse('signup'),
			{
				'email': 'new@example.com',
				'first_name': 'New',
				'last_name': 'User',
				'password1': self.password,
				'password2': self.password,
			},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('task_list'))
		self.assertTrue(get_user_model().objects.filter(email='new@example.com').exists())

	def test_login_with_valid_credentials_redirects_to_task_list(self):
		response = self.client.post(
			reverse('login'),
			{'username': self.user.email, 'password': self.password},
		)

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('task_list'))

	def test_login_with_invalid_credentials_renders_form(self):
		response = self.client.post(
			reverse('login'),
			{'username': self.user.email, 'password': 'WrongPassword!'},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Invalid email or password. Please try again.')

	def test_authenticated_user_visiting_login_is_redirected(self):
		self.client.force_login(self.user)

		response = self.client.get(reverse('login'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('task_list'))

	def test_logout_via_get_redirects_without_logging_out(self):
		self.client.force_login(self.user)

		response = self.client.get(reverse('logout'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('task_list'))

		protected = self.client.get(reverse('task_list'))
		self.assertNotIn(reverse('login'), protected.url if protected.status_code == 302 else '')

	def test_logout_via_post_logs_user_out(self):
		self.client.force_login(self.user)

		response = self.client.post(reverse('logout'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('login'))

		protected = self.client.get(reverse('task_list'))
		self.assertEqual(protected.status_code, 302)
		self.assertIn(reverse('login'), protected.url)
