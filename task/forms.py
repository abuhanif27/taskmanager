from django import forms
from . import models


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        fields = ['title', 'description', 'category', 'completed']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100 dark:placeholder:text-slate-500',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100 dark:placeholder:text-slate-500',
                'placeholder': 'Enter task description',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100'
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-300 text-brand-600 focus:ring-2 focus:ring-brand-400 dark:border-slate-700 dark:bg-slate-900'
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
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition placeholder:text-slate-400 focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100 dark:placeholder:text-slate-500',
            }
        ),
    )
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(
            attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100',
            }
        ),
    )
    category = forms.ChoiceField(
        required=False,
        choices=(),
        widget=forms.Select(
            attrs={
                'class': 'w-full rounded-xl border border-slate-300 bg-white/90 px-4 py-2.5 text-slate-900 shadow-sm transition focus:border-brand-500 focus:outline-none focus:ring-2 focus:ring-brand-400/40 dark:border-slate-700 dark:bg-slate-900/70 dark:text-slate-100',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].initial = self.STATUS_ALL
        self.fields['category'].choices = [('', 'All categories'), *models.Task.Category.choices]
