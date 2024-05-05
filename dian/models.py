from django.db import models


class DianDoc(models.Model):
    title = models.CharField(
        max_length=100,
        choices=[
            ("Informe de Gestión", "Informe de Gestión"),
            ("Certificado de Antecedentes", "Certificado de Antecedentes"),
            ("Certificado Cumplimiento Requesitos", "Certificado Cumplimiento Requesitos"),
            ("Estado de Resultados", "Estado de Resultados"),
            ("Estado Situación Financiera", "Estado Situación Financiera"),
            ("Certificado Cámara de Comercio", "Certificado Cámara de Comercio"),
        ],
    )
    year = models.IntegerField()
    file = models.FileField(upload_to="dian-docs")
