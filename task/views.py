from django.shortcuts import render, get_list_or_404
from . import models

# Create your views here.
def task_list(request):
    tasks = get_list_or_404(models.Task)
    return render(request, 'task/task_list.html', {'tasks': tasks})
