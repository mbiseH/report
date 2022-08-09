from django.contrib import admin
from CRUD_BACKEND.models import role, tasks, project, user, report


admin.site.register(role)
admin.site.register(tasks)
admin.site.register(project)
admin.site.register(user)
admin.site.register(report)
