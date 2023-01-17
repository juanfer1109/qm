from django.contrib import admin

from .models import Equip, Maintenance, Supplier

class equipAdmin(admin.ModelAdmin):
    list_display = ('name', 'next_maintenance',)
    list_filter = ('name', 'next_maintenance',)
    verbose_name_plural = 'Equipos'

class maintenanceAdmin(admin.ModelAdmin):
    list_display = ('equip', 'user', 'date',)
    list_filter = ('equip', 'user',)
    verbose_name_plural = 'Mantenimientos'

class supplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact',)
    verbose_name_plural = 'Proveedores'

admin.site.register(Equip, equipAdmin)
admin.site.register(Maintenance, maintenanceAdmin)
admin.site.register(Supplier, supplierAdmin)