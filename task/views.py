from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from . import models

# Create your views here.


def paginate_tasks(request, queryset, per_page=10):
    paginator = Paginator(queryset, per_page)
    page_param = request.GET.get('page', '1')

    try:
        page_number = int(page_param)
    except (TypeError, ValueError):
        page_number = 1

    if page_number < 1:
        page_number = 1
    elif page_number > paginator.num_pages:
        page_number = paginator.num_pages

    return paginator.page(page_number)

@login_required
def task_list(request):
    task_queryset = models.Task.objects.filter(user=request.user).order_by('completed', '-created_at')
    tasks = paginate_tasks(request, task_queryset)
    return render(request, 'task/task_list.html', {'tasks': tasks})

@login_required
def add_task(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' added successfully.")
            return redirect(reverse('task_list'))
        messages.error(request, 'Could not add task. Please fix the form errors and try again.')
    return render(request, 'task/add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id, user=request.user)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully.")
            return redirect(reverse('task_list'))
        messages.error(request, 'Could not update task. Please fix the form errors and try again.')
    return render(request, 'task/edit_task.html', {'form': form, 'task': task})


@login_required
def task_toggle_complete(request, task_id):
    if request.method != 'POST':
        messages.error(request, 'Invalid request method for changing task status.')
        return redirect(reverse('task_list'))

    task = get_object_or_404(models.Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    if task.completed:
        messages.success(request, f"Task '{task.title}' marked as completed.")
    else:
        messages.success(request, f"Task '{task.title}' marked as pending.")
    return redirect(reverse('task_list'))


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(models.Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task_title = task.title
        task.delete()
        messages.success(request, f"Task '{task_title}' deleted successfully.")
        return redirect(reverse('task_list'))
    
    return render(request,'task/delete_task.html',{'task': task})


@login_required
def completed_tasks(request):
    task_queryset = models.Task.objects.filter(user=request.user, completed=True).order_by('-created_at')
    tasks = paginate_tasks(request, task_queryset)
    return render(request, 'task/completed_task.html', {'tasks': tasks})


@login_required
def pending_tasks(request):
    task_queryset = models.Task.objects.filter(user=request.user, completed=False).order_by('-created_at')
    tasks = paginate_tasks(request, task_queryset)
    return render(request, 'task/pending_task.html', {'tasks': tasks})