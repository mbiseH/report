from django.contrib import admin
from CRUD_BACKEND.models import role, task, project, user, report
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'role',
                ),
            },
        ),
    )


admin.site.register(role)
admin.site.register(task)
admin.site.register(report)
admin.site.register(project)
admin.site.register(user, CustomUserAdmin)
