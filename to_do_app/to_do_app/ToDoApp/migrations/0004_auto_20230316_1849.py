# Generated by Django 3.2.17 on 2023-03-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ToDoApp', '0003_task_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofileinformation',
            name='profile_picture',
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Un attempted', 'Un attempted'), ('Done', 'Done')], default='un attempted', max_length=15),
        ),
    ]