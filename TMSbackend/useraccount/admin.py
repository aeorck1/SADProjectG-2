from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from useraccount import models
from django.utils.translation import gettext as _
# Register your models here.

class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = (
        'email',    'name',         'is_active',
        'is_staff', 'is_superuser', 'date_joined',
        'last_login'
    )
    fieldsets = (
        (
            None, 
            {
                'fields': ('email', 'password')
            }
        ),

        (
            _("Bio Info"),
            {
                'fields': ('name', )
            }
        ),

        (
            _("Permissions"),
            {
                'fields': ('is_staff', 'is_superuser', 'is_active')
            }
        ),

        (
            _("Dates"),
            {
                'fields': ('last_login', )
            }
        )
    )

    add_fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password1', 'password2'),
                'classes': ('wide', )
            }
        ),
    )

admin.site.register(models.User, UserAdmin)