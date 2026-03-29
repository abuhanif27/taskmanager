from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import TaskFilterForm, TaskForm
from . import models

# Create your views here.


def paginate_tasks(request, queryset, per_page=1):
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


def apply_task_filters(queryset, query, status, category):
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))

    if status == TaskFilterForm.STATUS_COMPLETED:
        queryset = queryset.filter(completed=True)
    elif status == TaskFilterForm.STATUS_PENDING:
        queryset = queryset.filter(completed=False)

    if category:
        queryset = queryset.filter(category=category)

    return queryset

@login_required
def task_list(request):
    filter_form = TaskFilterForm(request.GET or None)

    if filter_form.is_valid():
        query = filter_form.cleaned_data['query']
        status = filter_form.cleaned_data['status'] or TaskFilterForm.STATUS_ALL
        category = filter_form.cleaned_data['category']
    else:
        query = ''
        status = TaskFilterForm.STATUS_ALL
        category = ''
        filter_form = TaskFilterForm(initial={'status': TaskFilterForm.STATUS_ALL})

    queryset = models.Task.objects.filter(user=request.user).order_by('completed', '-created_at')
    queryset = apply_task_filters(queryset, query=query, status=status, category=category)
    tasks = paginate_tasks(request, queryset)

    query_params = request.GET.copy()
    query_params.pop('page', None)

    context = {
        'tasks': tasks,
        'heading': 'All Tasks',
        'filter_form': filter_form,
        'querystring': query_params.urlencode(),
        'reset_url': request.path,
    }
    return render(request, 'task/task_list.html', context)

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