from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from .forms import TaskForm
from . import models


# Create your views here.
def task_list(request):
    tasks = models.Task.objects.all().order_by('-created_at')
    return render(request, 'task/task_list.html', {'tasks': tasks})


def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('task_list'))
    return render(request, 'task/add_task.html', {'form': TaskForm()})


def edit_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('task_list'))
    return render(request, 'task/edit_task.html', {'form': TaskForm(instance=task), 'task': task})


def task_toggle_complete(request, task_id):
    task = models.Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect(reverse('task_list'))


def delete_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect(reverse('task_list'))

    return render(request, 'task/delete_task.html', {'task': task})
