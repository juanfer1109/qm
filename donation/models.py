from django.db import models
from django.contrib.auth.models import User


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(blank=False, null=False)
    date = models.DateField(blank=False, null=False)

    class Meta:
        verbose_name_plural = "donations"


class Permanencia(models.Model):
    year = models.PositiveSmallIntegerField(blank=False, null=False)
    formulario = models.CharField(max_length=14, blank=False, null=False)

    class Meta:
        verbose_name_plural = "permanencia"
