from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Task
from .forms import TaskForm
from datetime import date

class TaskViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            due_date=timezone.now().date(),
            priority="medium"
        )

    def test_task_calendar_view(self):
        response = self.client.get(reverse('task_calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/calendar.html')
        self.assertIn('tasks', response.context)
        self.assertQuerysetEqual(response.context['tasks'], Task.objects.all(), ordered=False)

    def test_create_task_view_get(self):
        test_date = date(2023, 5, 1)
        response = self.client.get(reverse('create_task', args=[test_date]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/create_task.html')
        self.assertIsInstance(response.context['form'], TaskForm)
        self.assertEqual(response.context['date'], test_date)

    def test_create_task_view_post_valid(self):
        test_date = date(2023, 5, 1)
        task_data = {
            'title': 'New Task',
            'description': 'This is a new task',
            'priority': 'high'
        }
        response = self.client.post(reverse('create_task', args=[test_date]), data=task_data)
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(title='New Task', due_date=test_date).exists())

    def test_create_task_view_post_invalid(self):
        test_date = date(2023, 5, 1)
        task_data = {
            'title': '',  # Invalid: empty title
            'description': 'This is a new task',
            'priority': 'high'
        }
        response = self.client.post(reverse('create_task', args=[test_date]), data=task_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/create_task.html')
        self.assertFalse(Task.objects.filter(description='This is a new task').exists())

    def test_task_list_view(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_list.html')
        self.assertIn('tasks', response.context)
        self.assertQuerysetEqual(response.context['tasks'], Task.objects.all(), ordered=False)

    def test_task_list_view_empty(self):
        Task.objects.all().delete()
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_list.html')
        self.assertQuerysetEqual(response.context['tasks'], [])

    def test_task_detail_view(self):
        response = self.client.get(reverse('task_detail', args=[self.task.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'task_manager/task_detail.html')
        self.assertEqual(response.context['task'], self.task)

    def test_task_detail_view_404(self):
        non_existent_id = 9999
        response = self.client.get(reverse('task_detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, 404)