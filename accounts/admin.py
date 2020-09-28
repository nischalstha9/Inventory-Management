from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('_type', 'email', 'password', 'first_name','last_name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active', 
            'is_staff', 
            'is_superuser',
            'groups', 
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('first_name','last_name','email','_type', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active','_type', 'groups')
    search_fields = ('email','first_name','last_name')
    ordering = ('first_name','last_name','email')
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
# admin.site.register(Student)
# admin.site.register(StudentProfile)