

from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser


class role(models.Model):
    role_id = models.BigAutoField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_creation_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.role_name



class user(AbstractUser):
    role = models.ForeignKey(role,null=True, on_delete=models.SET_NULL)
    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    def str(self):
            return self.username





class project_categories(models.Model):
    category_id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=255, unique=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['category_name']
    def str(self):
            return self.category_name


class status(models.Model):
    status_id = models.BigAutoField(primary_key=True)
    status_name = models.CharField(max_length=255, unique=True)
    status_description = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['status_name']
    def str(self):
            return self.status_name



class project(models.Model):
    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=255,  unique=True)
    project_members = models.ManyToManyField(user, related_name = 'project_members_for_a_particular_project', default=None)
    project_start_date = models.DateField(auto_now_add=True)
    project_end_date = models.DateField()
    project_client = models.CharField(max_length=255)
    project_description = models.CharField(null=False, max_length=255)
    project_comments = models.CharField(max_length=255)
    project_remarks = models.CharField(max_length=255)
    project_status = models.ForeignKey(status, null=True, default=None, on_delete=models.SET_NULL)
    project_category = models.ForeignKey(project_categories, on_delete=models.SET_NULL, null=True)
    project_leader = models.ForeignKey(user, null=True, on_delete=models.CASCADE)


    class Meta:
        ordering = ['project_name']
    def str(self):
            return self.project_name


class enrollment(models.Model):
    enrollment_id = models.BigAutoField(primary_key=True)
    project_id = models.ForeignKey(project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    project_name = models.CharField(max_length=255)




class task(models.Model):
    task_id = models.BigAutoField(primary_key=True)
    task_description = models.CharField(max_length=255, unique=True)
    task_start_date = models.DateField()
    task_completion_date = models.DateField()
    task_status = models.ForeignKey(status,null=True, on_delete=models.SET_NULL)
    task_blocking_issue = models.CharField(max_length=255, default=None, null=True)
    project_id = models.ForeignKey(project, on_delete=models.CASCADE)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-task_start_date']

class report(models.Model):
    report_id = models.BigAutoField(primary_key=True)
    report_creation_date= models.DateTimeField(auto_now_add=True)
    report_start_date = models.DateField()
    report_end_date = models.DateField()
    task_description = models.CharField(max_length=255)
    task_start_date = models.DateField()
    task_completion_date = models.DateField()
    task_status = models.CharField(max_length=50)
    project_name = models.CharField(max_length=255,  unique=True)
    # project_members = models.
    project_status = models.CharField(max_length=255)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    project_client = models.CharField(max_length=255)
    project_description = models.CharField(null=False, max_length=255)
    project_comments = models.CharField(max_length=255)
    project_remarks = models.CharField(max_length=255)
    project_leader = models.ForeignKey(user, null=True, on_delete=models.CASCADE)




