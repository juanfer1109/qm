from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import Donation, Permanencia

class donationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user', 'value', 'date',)
    list_filter = ('user', 'value', 'date',)
    verbose_name_plural = 'donations'

class permanenciaAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('year', 'formulario',)
    list_filter = ('year', 'formulario',)
    verbose_name_plural = 'permanencia'

admin.site.register(Donation, donationAdmin)
admin.site.register(Permanencia, permanenciaAdmin)