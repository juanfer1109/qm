from django.contrib import admin
from .models import TipoDocumento, Documento
from import_export.admin import ExportActionMixin

class TipoDocumentoAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "tipo",
    )
    
    list_filter = ("tipo",)
    
class DocumentoAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = (
        "nombre",
        "tipo",
    )
    
    list_filter = ("nombre",
                   "tipo",
    )

admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(Documento, DocumentoAdmin)