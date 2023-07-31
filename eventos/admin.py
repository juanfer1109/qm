from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import Evento, Inscripciones


class eventAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "nombre",
        "fecha",
    )
    list_filter = (
        "concluido",
        "cancelado",
    )
    verbose_name_plural = "eventos"


class inscripcionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("usuario", "evento", "pago_recibido")
    list_filter = (
        "usuario",
        "evento",
    )
    verbose_name_plural = "inscripciones"


admin.site.register(Evento, eventAdmin)
admin.site.register(Inscripciones, inscripcionAdmin)
