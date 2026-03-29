from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_assign_unowned_tasks'),
    ]

    operations = [
        migrations.AddField(
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
                db_index=True,
                default='general',
                max_length=20,
            ),
        ),
    ]
