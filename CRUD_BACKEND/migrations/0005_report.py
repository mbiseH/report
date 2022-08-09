# Generated by Django 3.2.12 on 2022-08-09 13:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CRUD_BACKEND', '0004_alter_tasks_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='report',
            fields=[
                ('report_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('report_creation_date', models.DateTimeField(auto_now_add=True)),
                ('report_start_date', models.DateField()),
                ('report_end_date', models.DateField()),
                ('task_description', models.CharField(max_length=255)),
                ('task_start_date', models.DateField()),
                ('task_completion_date', models.DateField()),
                ('task_status', models.CharField(max_length=50)),
                ('project_name', models.CharField(max_length=255, unique=True)),
                ('project_status', models.CharField(max_length=255)),
                ('project_start_date', models.DateField(auto_now_add=True)),
                ('project_end_date', models.DateField()),
                ('project_client', models.CharField(max_length=255)),
                ('project_description', models.CharField(max_length=255)),
                ('project_comments', models.CharField(max_length=255)),
                ('project_remarks', models.CharField(max_length=255)),
                ('project_leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
