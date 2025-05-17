from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import Equip, Maintenance, Supplier


class equipAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "responsable",
        "next_maintenance",
    )
    list_filter = (
        "name",
        "next_maintenance",
    )
    verbose_name_plural = "Equipos"


class maintenanceAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "equip",
        "user",
        "date",
    )
    list_filter = (
        "equip",
        "user",
    )
    verbose_name_plural = "Mantenimientos"


class supplierAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "name",
        "contact",
    )
    verbose_name_plural = "Proveedores"


admin.site.register(Equip, equipAdmin)
admin.site.register(Maintenance, maintenanceAdmin)
admin.site.register(Supplier, supplierAdmin)
