from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User

from .models import CustomUser

class UserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'CustomUsers'

class CustomUserAdmin(UserAdmin):
    inlines = (UserInline, )

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)