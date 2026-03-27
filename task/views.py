from django.shortcuts import redirect, render
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