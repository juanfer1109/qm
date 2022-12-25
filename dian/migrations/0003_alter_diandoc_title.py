# Generated by Django 4.1.3 on 2022-12-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dian', '0002_rename_diandocs_diandoc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diandoc',
            name='title',
            field=models.CharField(choices=[('Informe de Gestión', 'Informe de Gestión'), ('cert_antec', 'Certificado de Atecedentes'), ('cert_cump', 'Certificado Cumplimiento Requesitos'), ('pyg', 'Estado de Resultados'), ('balance', 'Estado Situación Financiera'), ('camara', 'Certificado Cámara de Comercio')], max_length=100),
        ),
    ]