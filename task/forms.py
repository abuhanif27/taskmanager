from django import forms
from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'category', 'completed']
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
            'category': forms.Select(attrs={
                'class': 'w-full mb-4 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 mb-4 text-blue-600 rounded focus:ring-2 focus:ring-blue-500'
            })
        }


class TaskFilterForm(forms.Form):
    STATUS_ALL = 'all'
    STATUS_COMPLETED = 'completed'
    STATUS_PENDING = 'pending'

    STATUS_CHOICES = (
        (STATUS_ALL, 'All statuses'),
        (STATUS_COMPLETED, 'Completed'),
        (STATUS_PENDING, 'Pending'),
    )

    query = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search title or description',
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }
        ),
    )
    category = forms.ChoiceField(
        required=False,
        choices=(),
        widget=forms.Select(
            attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = self.STATUS_ALL
        self.fields['category'].choices = [('', 'All categories'), *models.Task.Category.choices]
