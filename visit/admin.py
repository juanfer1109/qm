from django.contrib import admin
from .models import MoneyMovement, Visit, VisitCalendar
from import_export.admin import ExportActionMixin


class movementInLineAdmin(admin.TabularInline):
    model = MoneyMovement
    list_display = (
        "visit",
        "categoria",
        "valor",
    )
    list_filter = ("visit",)


class movementAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "visit",
        "categoria",
        "valor",
    )
    list_filter = ("visit",)


class visitAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "date",
        "visitor",
    )
    list_filter = ("visitor",)
    inlines = [
        movementInLineAdmin,
    ]


class CalendarAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "visitor",
        "date",
    )
    list_filter = ("visitor",)


admin.site.register(Visit, visitAdmin)
admin.site.register(MoneyMovement, movementAdmin)
admin.site.register(VisitCalendar, CalendarAdmin)
