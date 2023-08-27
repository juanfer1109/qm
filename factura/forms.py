from django import forms

from .models import Factura


class facturaForm(forms.ModelForm):
    # category = forms.CharField(required=True)
    # value = forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = Factura
        fields = (
            "proveedor",
            "date",
            "numero",
            "valor",
        )