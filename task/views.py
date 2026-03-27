from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from .forms import TaskForm
from . import models


# Create your views here.
def task_list(request):
    tasks = models.Task.objects.all().order_by('-created_at')
    return render(request, 'task/task_list.html', {'tasks': tasks})


def add_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"Task '{task.title}' added successfully.")
            return redirect(reverse('task_list'))
        messages.error(request, 'Could not add task. Please fix the form errors and try again.')
    return render(request, 'task/add_task.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully.")
            return redirect(reverse('task_list'))
        messages.error(request, 'Could not update task. Please fix the form errors and try again.')
    return render(request, 'task/edit_task.html', {'form': form, 'task': task})


def task_toggle_complete(request, task_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid request method for changing task status.')
        return redirect(reverse('task_list'))

    task = get_object_or_404(models.Task, id=task_id)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, f"Task '{task.title}' marked as completed.")
    else:
        messages.success(request, f"Task '{task.title}' marked as pending.")
    return redirect(reverse('task_list'))


def delete_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f"Task '{task_title}' deleted successfully.")
        return redirect(reverse('task_list'))

    return render(request, 'task/delete_task.html', {'task': task})


def completed_tasks(request):
    tasks = models.Task.objects.filter(completed=True).order_by('-created_at')
    return render(request, 'task/completed_task.html', {'tasks': tasks})


def pending_tasks(request):
    tasks = models.Task.objects.filter(completed=False).order_by('-created_at')
    return render(request, 'task/pending_task.html', {'tasks': tasks})
