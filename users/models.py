from django.contrib.auth.models import User
from django.db import models

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(blank=False, max_length=10)
    # first_name = models.CharField(max_length=150, blank=False, null=True)
    # last_name = models.CharField(max_length=150, blank=False)
    # email = models.EmailField(blank=False, unique=True)
    birthday = models.DateField()
    gender = models.CharField(
        max_length=10,
        choices=[('Hombre', 'Hombre'), ('Mujer', 'Mujer'), ('No Binario', 'No Binario')]
    )

    def __str__(self):
        return self.user.username