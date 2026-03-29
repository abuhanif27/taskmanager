from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.CharField(
                choices=[
                    ('general', 'General'),
                    ('work', 'Work'),
                    ('personal', 'Personal'),
                    ('study', 'Study'),
                    ('health', 'Health'),
                ],
                default='general',
                max_length=20,
            ),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['user', 'completed', 'category'], name='task_user_compl_4c3dc8_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['user', '-created_at'], name='task_user_created_c4f96f_idx'),
        ),
    ]
