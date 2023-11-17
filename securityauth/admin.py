from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

# Register your models here.
class CustomUserAdmin(UserAdmin):
  # Customize the display fields for the user list page
  list_display = ('username', 'email', 'is_allowed')

  # Customize the fields displayed on the user edit page
  fieldsets = (
    (None, {'fields': ('username', 'password')}),
    ('Allow User To Access', {'fields': ('is_allowed',)}),
    ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    ('Important Dates', {'fields': ('last_login', 'date_joined')}),
  )

admin.site.register(CustomUser, CustomUserAdmin)
