from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(models.Model):
    DOC_TYPES = [
        ("cc", "Cédula Ciudadanía"),
        ("ti", "Tarjeda de Identidad"),
        ("ce", "Cédula Extranjería"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doc_type = models.CharField(max_length=5, default="", blank=True, choices=DOC_TYPES)
    id_number = models.PositiveBigIntegerField(default=None, blank=True, null=True)
    phone_number = models.PositiveBigIntegerField()
    nickname = models.CharField(blank=False, max_length=20)
    birthday = models.DateField()
    mailing_list = models.BooleanField()
    info_manage = models.BooleanField()
    comunidad = models.BooleanField(default=False)
    publicar = models.BooleanField(default=False)
    tiene_reclamacion = models.BooleanField(default=False)
    mtto = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    visit_resp = models.BooleanField(default=False)
    pareja = models.OneToOneField("self", blank=True, null=True, on_delete=models.CASCADE, related_name="pareja_inversa" )

    def __str__(self):
        return self.user.username
