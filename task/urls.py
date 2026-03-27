from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('tasks/toggle/<int:task_id>/', views.task_toggle_complete, name='task_toggle_complete'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('tasks/completed/', views.completed_tasks, name='completed_tasks'),
    path('tasks/pending/', views.pending_tasks, name='pending_tasks'),
]
