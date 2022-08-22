# Generated by Django 3.2.12 on 2022-08-16 14:03

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('project_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(max_length=255, unique=True)),
                ('project_status', models.CharField(max_length=255)),
                ('project_start_date', models.DateField(auto_now_add=True)),
                ('project_end_date', models.DateField()),
                ('project_client', models.CharField(max_length=255)),
                ('project_description', models.CharField(max_length=255)),
                ('project_comments', models.CharField(max_length=255)),
                ('project_remarks', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='role',
            fields=[
                ('role_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('role_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='CRUD_BACKEND.role')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='tasks',
            fields=[
                ('task_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('task_description', models.CharField(max_length=255)),
                ('task_start_date', models.DateField()),
                ('task_completion_date', models.DateField()),
                ('task_status', models.CharField(max_length=50)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRUD_BACKEND.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
                ('project_start_date', models.DateField()),
                ('project_end_date', models.DateField()),
                ('project_client', models.CharField(max_length=255)),
                ('project_description', models.CharField(max_length=255)),
                ('project_comments', models.CharField(max_length=255)),
                ('project_remarks', models.CharField(max_length=255)),
                ('project_leader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='project_leader',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='project_members',
            field=models.ManyToManyField(default=None, related_name='project_members_for_a_particular_project', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='enrollment',
            fields=[
                ('enrollment_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('enrollment_date', models.DateTimeField(auto_now_add=True)),
                ('project_name', models.CharField(max_length=255)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CRUD_BACKEND.project')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
