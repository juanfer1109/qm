from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import Donation

class donationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('user', 'value', 'date',)
    list_filter = ('user', 'value', 'date',)
    verbose_name_plural = 'donations'

admin.site.register(Donation, donationAdmin)