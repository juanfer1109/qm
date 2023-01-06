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
    # list_display = ('username', 'first_name', 'last_name', 'nickname')
    # list_filter = ('comunidad', 'publicar', 'mtto', 'tiene_reclamacion')

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)