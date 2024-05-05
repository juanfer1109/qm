from django import forms

from .models import DianDoc

CHOICES=[
            ("Informe de Gestión", "Informe de Gestión"),
            ("Certificado de Antecedentes", "Certificado de Antecedentes"),
            ("Certificado Cumplimiento Requesitos", "Certificado Cumplimiento Requesitos"),
            ("Estado de Resultados", "Estado de Resultados"),
            ("Estado Situación Financiera", "Estado Situación Financiera"),
            ("Certificado Cámara de Comercio", "Certificado Cámara de Comercio"),
        ]

class DIANForm(forms.ModelForm):
    class Meta:
        model = DianDoc
        fields = {'title', 'year', 'file'}
        
    # title = forms.ChoiceField(choices=CHOICES)
    # year = forms.IntegerField()
    # file = forms.FileField()