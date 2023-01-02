from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.PositiveBigIntegerField()
    nickname = models.CharField(blank=False, max_length=20)
    birthday = models.DateField()
    mailing_list = models.BooleanField()
    info_manage = models.BooleanField()
    comunidad = models.BooleanField(default=False)
    publicar = models.BooleanField(default=False)
    tiene_reclamacion = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    