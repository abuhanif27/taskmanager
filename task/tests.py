from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskTestBase(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			email='alice@example.com',
			password='StrongPassword123!',
			first_name='Alice',
			last_name='Doe',
		)
		self.other_user = get_user_model().objects.create_user(
			email='bob@example.com',
			password='StrongPassword123!',
			first_name='Bob',
			last_name='Doe',
		)
		self.client.force_login(self.user)

	def create_task(self, **overrides):
		defaults = {
			'user': self.user,
			'title': 'Task title',
			'description': 'Task description',
			'category': Task.Category.GENERAL,
			'completed': False,
		}
		defaults.update(overrides)
		return Task.objects.create(**defaults)


class TaskListFilteringTests(TaskTestBase):
	def setUp(self):
		super().setUp()
		self.create_task(
			title='Ship release notes',
			description='Write and publish release notes',
			category=Task.Category.WORK,
			completed=False,
		)
		self.create_task(
			title='Morning run',
			description='Run 5km in the park',
			category=Task.Category.HEALTH,
			completed=True,
		)
		self.create_task(
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

	def test_search_is_case_insensitive(self):
		response = self.client.get(reverse('task_list'), {'query': 'MORNING'})

		self.assertContains(response, 'Morning run')
		self.assertNotContains(response, 'Ship release notes')

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

	def test_invalid_status_parameter_falls_back_to_unfiltered(self):
		response = self.client.get(reverse('task_list'), {'status': 'not-a-status'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ship release notes')
		self.assertContains(response, 'Morning run')
		self.assertContains(response, 'Read design patterns')

	def test_invalid_category_parameter_falls_back_to_unfiltered(self):
		response = self.client.get(reverse('task_list'), {'category': 'unknown-category'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Ship release notes')
		self.assertContains(response, 'Morning run')
		self.assertContains(response, 'Read design patterns')

	def test_conflicting_filters_return_empty_list(self):
		response = self.client.get(
			reverse('task_list'),
			{'status': 'completed', 'category': Task.Category.STUDY},
		)

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'No tasks found.')


class TaskPaginationTests(TaskTestBase):
	def setUp(self):
		super().setUp()
		for index in range(12):
			self.create_task(title=f'Task {index}')

	def test_invalid_page_uses_first_page(self):
		response = self.client.get(reverse('task_list'), {'page': 'invalid'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Page 1 of 2')

	def test_page_below_one_uses_first_page(self):
		response = self.client.get(reverse('task_list'), {'page': '-7'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Page 1 of 2')

	def test_page_above_max_uses_last_page(self):
		response = self.client.get(reverse('task_list'), {'page': '999'})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'Page 2 of 2')

	def test_pagination_links_preserve_filter_query_params(self):
		response = self.client.get(reverse('task_list'), {'status': 'pending', 'query': 'Task', 'page': '1'})

		self.assertContains(response, 'status=pending')
		self.assertContains(response, 'query=Task')


class TaskAuthorizationTests(TaskTestBase):
	def test_unauthenticated_user_is_redirected_for_protected_views(self):
		self.client.logout()

		response = self.client.get(reverse('task_list'))

		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse('login'), response.url)

	def test_task_list_shows_only_current_user_tasks(self):
		self.create_task(title='Visible task')
		self.create_task(user=self.other_user, title='Hidden task')

		response = self.client.get(reverse('task_list'))

		self.assertContains(response, 'Visible task')
		self.assertNotContains(response, 'Hidden task')

	def test_edit_foreign_task_returns_404(self):
		foreign_task = self.create_task(user=self.other_user, title='Foreign task')

		response = self.client.get(reverse('edit_task', kwargs={'task_id': foreign_task.id}))

		self.assertEqual(response.status_code, 404)

	def test_toggle_foreign_task_returns_404(self):
		foreign_task = self.create_task(user=self.other_user, title='Foreign task')

		response = self.client.post(reverse('task_toggle_complete', kwargs={'task_id': foreign_task.id}))

		self.assertEqual(response.status_code, 404)

	def test_delete_foreign_task_returns_404(self):
		foreign_task = self.create_task(user=self.other_user, title='Foreign task')

		response = self.client.post(reverse('delete_task', kwargs={'task_id': foreign_task.id}))

		self.assertEqual(response.status_code, 404)


class TaskMutationTests(TaskTestBase):
	def test_add_task_creates_record_for_logged_in_user(self):
		response = self.client.post(
			reverse('add_task'),
			{
				'title': 'New professional task',
				'description': 'Plan rollout',
				'category': Task.Category.WORK,
				'completed': '',
			},
		)

		self.assertEqual(response.status_code, 302)
		created = Task.objects.get(title='New professional task')
		self.assertEqual(created.user, self.user)
		self.assertEqual(created.category, Task.Category.WORK)
		self.assertFalse(created.completed)

	def test_edit_task_updates_category_and_completion(self):
		task = self.create_task(title='Needs update', category=Task.Category.GENERAL, completed=False)

		response = self.client.post(
			reverse('edit_task', kwargs={'task_id': task.id}),
			{
				'title': 'Needs update',
				'description': 'Updated details',
				'category': Task.Category.PERSONAL,
				'completed': 'on',
			},
		)

		self.assertEqual(response.status_code, 302)
		task.refresh_from_db()
		self.assertEqual(task.category, Task.Category.PERSONAL)
		self.assertTrue(task.completed)

	def test_toggle_complete_switches_task_status(self):
		task = self.create_task(completed=False)

		response = self.client.post(reverse('task_toggle_complete', kwargs={'task_id': task.id}))

		self.assertEqual(response.status_code, 302)
		task.refresh_from_db()
		self.assertTrue(task.completed)

	def test_toggle_complete_requires_post(self):
		task = self.create_task(completed=False)

		response = self.client.get(reverse('task_toggle_complete', kwargs={'task_id': task.id}))

		self.assertEqual(response.status_code, 302)
		task.refresh_from_db()
		self.assertFalse(task.completed)

	def test_delete_task_requires_post_confirmation(self):
		task = self.create_task(title='Delete me')

		response = self.client.get(reverse('delete_task', kwargs={'task_id': task.id}))

		self.assertEqual(response.status_code, 200)
		self.assertTrue(Task.objects.filter(id=task.id).exists())

	def test_delete_task_removes_record_on_post(self):
		task = self.create_task(title='Delete me now')

		response = self.client.post(reverse('delete_task', kwargs={'task_id': task.id}))

		self.assertEqual(response.status_code, 302)
		self.assertFalse(Task.objects.filter(id=task.id).exists())
