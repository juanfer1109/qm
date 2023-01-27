from django.contrib import admin
from .models import MoneyMovement, Visit
from import_export.admin import ExportActionMixin


class movementInLineAdmin(admin.TabularInline):
    model = MoneyMovement
    list_display = ('visit', 'categoria', 'valor',)
    list_filter = ('visit',)

class movementAdmin(ExportActionMixin ,admin.ModelAdmin):
    list_display = ('visit', 'categoria', 'valor',)
    list_filter = ('visit',)

class visitAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('date', 'visitor',)
    list_filter = ('visitor',)
    inlines = [movementInLineAdmin,]

admin.site.register(Visit, visitAdmin)
admin.site.register(MoneyMovement, movementAdmin)
