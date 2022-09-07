from django.contrib import admin
from CRUD_BACKEND.models import role, project_categories,status, task, project, user, report, enrollment
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Custom Field Heading',
            {
                'fields': (
                    'role',
                ),
            },
        ),
    )


admin.site.register(role)
admin.site.register(project_categories)
admin.site.register(status)
admin.site.register(task)
admin.site.register(project)
admin.site.register(enrollment)
admin.site.register(user, CustomUserAdmin)

# Register your models here.
