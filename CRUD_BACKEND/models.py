from tkinter import CASCADE
from django.db import models
from django.db import models
# from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_description = models.CharField(max_length=255)
    role_title = models.CharField(max_length=50)


class projects(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=50)
    project_members = models.ManyToManyField(max_length=255)
    project_creation_date = models.DateTimeField(auto_now_add=True)
    project_completion_date = models.DateField()


class reporting(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    blocking_issues = models.ManyToManyField(max_length=255)
    project_id = models.ForeignKey(projects, on_delete=CASCADE)


class user(AbstractUser):

    user_password_reset_code = models.CharField(max_length= 20, blank = True)
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username
