from django import forms
from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Enter task description',
                'rows': 4
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 mb-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            })
        }
