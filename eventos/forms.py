from django import forms

from .models import Evento

class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = {'nombre', 'tipo', 'descripcion', 'lugar', 'duracion', 'incluye', 'fecha', 
                  'costo1', 'fecha_costo1', 'costo2', 'fecha_costo2', 'costo', 'fecha_costo',
                  'imagen', 'cupos', 'prueba', 'cancelado'}
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "fecha_costo1": forms.DateInput(attrs={"type": "date"}),
            "fecha_costo2": forms.DateInput(attrs={"type": "date"}),
            "fecha_costo": forms.DateInput(attrs={"type": "date"}),
        }
        