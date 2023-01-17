from django.contrib.auth.models import User
from django.db import models

class Equip(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    frequency = models.PositiveSmallIntegerField()
    last_maintenance = models.DateField(null=True, blank=True)
    next_maintenance = models.DateField(null=True, blank=True)
    last_value = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'equipos'

class Supplier(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=100)
    phone_number = models.PositiveIntegerField()
    contact = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta():
        verbose_name_plural = 'Proveedores'

class Maintenance(models.Model):
    equip = models.ForeignKey(Equip, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    date = models.DateField()
    value = models.PositiveIntegerField()
    notes = models.TextField()

    class Meta():
        verbose_name_plural = 'Mantenimientos'