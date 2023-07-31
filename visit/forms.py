from django import forms
from django.forms.models import inlineformset_factory

from .models import MoneyMovement, Visit


class MoneyMovementForm(forms.ModelForm):
    # category = forms.CharField(required=True)
    # value = forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = MoneyMovement
        fields = (
            "categoria",
            "valor",
        )


MovementFormSet = inlineformset_factory(
    Visit,
    MoneyMovement,
    MoneyMovementForm,
    can_delete=False,
    min_num=0,
    extra=9,
)
