from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Task


class TaskListFilteringTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			email='alice@example.com',
			password='StrongPassword123!',
			first_name='Alice',
			last_name='Doe',
		)
		self.client.force_login(self.user)

		Task.objects.create(
			user=self.user,
			title='Ship release notes',
			description='Write and publish release notes',
			category=Task.Category.WORK,
			completed=False,
		)
		Task.objects.create(
			user=self.user,
			title='Morning run',
			description='Run 5km in the park',
			category=Task.Category.HEALTH,
			completed=True,
		)
		Task.objects.create(
			user=self.user,
			title='Read design patterns',
			description='Study chapter 4',
			category=Task.Category.STUDY,
			completed=False,
		)

	def test_search_filters_by_title_and_description(self):
		response = self.client.get(reverse('task_list'), {'query': 'release'})

		self.assertContains(response, 'Ship release notes')
		self.assertNotContains(response, 'Morning run')
		self.assertNotContains(response, 'Read design patterns')

	def test_status_filter_returns_only_completed_tasks(self):
		response = self.client.get(reverse('task_list'), {'status': 'completed'})

		self.assertContains(response, 'Morning run')
		self.assertNotContains(response, 'Ship release notes')
		self.assertNotContains(response, 'Read design patterns')

	def test_category_filter_returns_only_selected_category(self):
		response = self.client.get(reverse('task_list'), {'category': Task.Category.STUDY})

		self.assertContains(response, 'Read design patterns')
		self.assertNotContains(response, 'Ship release notes')
		self.assertNotContains(response, 'Morning run')

	def test_combined_filters_apply_together(self):
		response = self.client.get(
			reverse('task_list'),
			{'query': 'run', 'status': 'completed', 'category': Task.Category.HEALTH},
		)

		self.assertContains(response, 'Morning run')
		self.assertNotContains(response, 'Ship release notes')
		self.assertNotContains(response, 'Read design patterns')
