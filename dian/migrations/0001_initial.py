# Generated by Django 4.1.3 on 2023-01-08 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DianDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Informe de Gestión', 'Informe de Gestión'), ('Certificado de Atecedentes', 'Certificado de Atecedentes'), ('Certificado Cumplimiento Requesitos', 'Certificado Cumplimiento Requesitos'), ('Estado de Resultados', 'Estado de Resultados'), ('Estado Situación Financiera', 'Estado Situación Financiera'), ('Certificado Cámara de Comercio', 'Certificado Cámara de Comercio')], max_length=100)),
                ('year', models.IntegerField()),
                ('file', models.FileField(upload_to='dian-docs')),
            ],
        ),
    ]
