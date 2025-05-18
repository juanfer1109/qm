from django.db import models
import os
from django.conf import settings


from users.models import CustomUser

class TipoDocumento(models.Model):
    tipo = models.CharField("Tipo Documento", max_length=80, blank=False, null=False, unique=True)
    
    def __str__(self):
        return self.tipo
    
    class Meta:
        verbose_name_plural = "tipos de documento"


class Documento(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    nombre = models.CharField("Nombre", max_length=50, blank=False, null=False)
    date = models.DateField("Fecha Documento", blank=False, null=False)
    file = models.FileField(upload_to="documentos")
    tipo = models.ForeignKey(TipoDocumento, on_delete=models.CASCADE)
    
    def delete(self, *args, **kwargs):
        os.remove(os.path.join(settings.MEDIA_ROOT, self.file.name))
        super(Documento,self).delete(*args,**kwargs)

    class Meta:
        verbose_name_plural = "documentos"
        
