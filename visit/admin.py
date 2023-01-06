from django.contrib import admin
from .models import MoneyMovement, Visit


class movementInLineAdmin(admin.TabularInline):
    model = MoneyMovement
    list_display = ('visit', 'category', 'value',)
    list_filter = ('visit',)

class visitAdmin(admin.ModelAdmin):
    list_display = ('date', 'visitor',)
    list_filter = ('visitor',)
    inlines = [movementInLineAdmin,]


admin.site.register(Visit, visitAdmin)

