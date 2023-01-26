from django.db import models
from django.contrib.auth.models import User

class Evento(models.Model):
    TYPES = [
        ('Taller', 'Taller'),
        ('Encuentro', 'Encuentro'),
        ('Experiencia', 'Experiencia'),
    ]
    
    nombre = models.CharField(max_length=40)
    tipo = models.CharField(max_length=15, choices=TYPES)
    descripcion = models.TextField(null=True, blank=True)
    lugar = models.TextField(null=True, blank=True)
    duracion = models.CharField(max_length=40)
    incluye = models.TextField(null=True, blank=True)
    fecha = models.DateField()
    costo1 = models.PositiveIntegerField(default=0)
    fecha_costo1 = models.DateField(default=None, null=True, blank=True)
    costo2 = models.PositiveIntegerField(default=0)
    fecha_costo2 = models.DateField(default=None, null=True, blank=True)
    costo = models.PositiveIntegerField(default=0)
    fecha_costo = models.DateField(default=None, null=True, blank=True)
    imagen = models.ImageField(upload_to='eventos', null=True, blank=True)
    inscritos = models.ManyToManyField(User, blank=True)
    concluido = models.BooleanField(default=False)
    cancelado = models.BooleanField(default=False)
    cupos = models.PositiveSmallIntegerField(default=0)
    cant_inscritos = models.PositiveSmallIntegerField(default=0)
    cerrado = models.BooleanField(default=False)
    prueba = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Inscripciones(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    pago_recibido = models.BooleanField(default=False)
    factura = models.BooleanField(default=False)
    cantidad = models.PositiveSmallIntegerField(default=1)

    class Meta():
        verbose_name_plural = 'inscripciones'