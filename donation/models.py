from django.db import models
from django.contrib.auth.models import User

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(blank=False, null=False)
    date = models.DateField(blank=False, null=False)

    class Meta():
        verbose_name_plural = 'donations'