from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import Factura


class facturasAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "user",
        "date",
        "proveedor",
        "numero",
        "valor",
        "pagada",
    )
    list_filter = ("user", "pagada")
    
admin.site.register(Factura, facturasAdmin)