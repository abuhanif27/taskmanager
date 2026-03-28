from django.conf import settings
from django.db import migrations


def assign_unowned_tasks(apps, schema_editor):
    task_model = apps.get_model('task', 'Task')
    user_model = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))

    fallback_user = user_model.objects.filter(is_superuser=True).order_by('id').first()
    if fallback_user is None:
        fallback_user = user_model.objects.order_by('id').first()

    if fallback_user is None:
        return

    task_model.objects.filter(user__isnull=True).update(user=fallback_user)


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_task_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(assign_unowned_tasks, migrations.RunPython.noop),
    ]
