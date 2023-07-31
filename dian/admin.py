from django.contrib import admin

from .models import DianDoc


class DianDocsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "year",
    )
    list_filter = (
        "title",
        "year",
    )
    search_fields = [
        "title",
        "year",
    ]


admin.site.register(DianDoc, DianDocsAdmin)
