from django.db import models

from users.models import CustomUser


class Factura(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    proveedor = models.CharField("Proveedor", max_length=50, blank=False, null=False)
    date = models.DateField("Fecha Factura", blank=False, null=False)
    numero = models.CharField("Número Factura", max_length=15, blank=False, null=False)
    valor = models.PositiveBigIntegerField("Valor", blank=False, null=False)
    pagada = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "facturas"
