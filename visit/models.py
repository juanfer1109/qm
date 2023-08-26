from django.db import models

from users.models import CustomUser


class Visit(models.Model):
    visitor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    notes = models.TextField()
    total_balance = models.IntegerField(default=0)
    facturas_elec = models.IntegerField(default=0)
    revisado = models.BooleanField(default=False)

    class Meta:
        ordering = ["date"]


class MoneyMovement(models.Model):
    TYPES = [("Ingreso", "Ingreso"), ("Egreso", "Egreso")]
    CATEGORIES = [
        ("venta_huevos", "Venta huevos"),
        ("venta_huerta", "Venta huerta"),
        ("insumos_gallinas", "Insumos gallinas"),
        ("insumos_huerta", "Insumos huerta"),
        ("cuido_perros", "Cuido perros"),
        ("gasolina", "Gasolina"),
        ("cafeteria", "Insumos cafetería"),
        ("aseo", "Insumos aseo"),
        ("otros_ingresos", "Otros Ingresos"),
        ("otros_gastos", "Otros Gastos"),
    ]

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    categoria = models.CharField(
        max_length=20, choices=CATEGORIES, default="venta_huevos"
    )
    valor = models.PositiveBigIntegerField()
    fact_elec = models.BooleanField('Factura Electrónica', default=False)

    class Meta:
        ordering = ["visit"]

    def __str__(self):
        return self.categoria


class VisitCalendar(models.Model):
    visitor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
