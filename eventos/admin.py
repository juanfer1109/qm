from django.contrib import admin

from .models import Evento, Inscripciones

class eventAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha',)
    list_filter = ('concluido', 'cancelado',)
    verbose_name_plural = 'eventos'

class inscripcionAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'evento',)
    list_filter = ('usuario', 'evento',)
    verbose_name_plural = 'inscripciones'

admin.site.register(Evento, eventAdmin)
admin.site.register(Inscripciones, inscripcionAdmin)