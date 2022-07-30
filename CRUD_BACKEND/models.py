from django.db import models
from django.contrib.auth.models import AbstractUser
# from .models import User



class role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=255, choices=[("Prog.", "Programmer"), ('BA', 'Business Analyst'), ('Mgr','Manager')])


class user(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, verbose_name="email address")
    # role = models.ForeignKey(role, on_delete=models.SET_DEFAULT)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"


class project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_members = models.ManyToManyField(user, related_name = 'project_members_for_a_particular_project' )
    project_status = models.CharField(max_length=255)
    project_start_date = models.DateField(auto_now_add=True)
    project_end_date = models.DateField()
    project_client = models.CharField(max_length=255)
    project_description = models.CharField(null=False, max_length=255)
    project_comments = models.CharField(max_length=255)
    project_remarks = models.CharField(max_length=255)
    project_leader = models.CharField(max_length=255)



class tasks(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_description = models.CharField(max_length=255)
    task_start_date = models.DateField()
    task_completion_date = models.DateField()
    task_status = models.CharField(max_length=50)
    associated_project = models.ForeignKey(project, on_delete=models.CASCADE)



class report(project, tasks):
    report_id = models.BigAutoField(primary_key=True)
    report_creation_date= models.DateTimeField(auto_now_add=True)
    report_start_date = models.DateField()
    report_end_date = models.DateField()

