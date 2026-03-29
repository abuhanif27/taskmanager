from django.db import models
from taskmanager.settings import AUTH_USER_MODEL


# Create your models here.
class Task(models.Model):
    class Category(models.TextChoices):
        GENERAL = 'general', 'General'
        WORK = 'work', 'Work'
        PERSONAL = 'personal', 'Personal'
        STUDY = 'study', 'Study'
        HEALTH = 'health', 'Health'

    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.GENERAL)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'completed', 'category']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return self.title