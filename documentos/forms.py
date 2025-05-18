from django import forms

from .models import TipoDocumento, Documento


class TipoForm(forms.ModelForm):
    class Meta:
        model = TipoDocumento
        fields = {'tipo'}
        

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = {'nombre', 'date', 'file', 'tipo'}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }