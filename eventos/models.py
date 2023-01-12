from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    TYPES = [
        ('Taller', 'Taller'),
        ('Encuentro', 'Encuentro'),
    ]
    
    nombre = models.CharField(max_length=40)
    tipo = models.CharField(max_length=15, choices=TYPES)
    descripcion = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    costo = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='eventos', null=True, blank=True)
    inscritos = models.ManyToManyField(User, blank=True)
    concluido = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    cupos = models.PositiveSmallIntegerField(default=0)
    cant_inscritos = models.PositiveSmallIntegerField(default=0)
    cerrado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Inscripciones(models.Model):
    FORMA_PAGO = [
        ('Efectivo', 'Efectivo'),
        ('Consignacion', 'Consignación'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    forma_pago = models.CharField(max_length=20, choices=FORMA_PAGO)
    pago_recibido = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)

    class Meta():
        verbose_name_plural = 'inscripciones'