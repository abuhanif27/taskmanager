from django.shortcuts import render
from . import models

# Create your views here.
def task_list(request):
    tasks = models.Task.objects.all()
    return render(request, 'task/task_list.html', {'tasks': tasks})
