# Generated by Django 4.1.5 on 2023-04-24 15:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0014_inscripciones_cantidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripciones',
            name='valor_recibido',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inscripciones',
            name='valor_segun_fecha',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='inscripciones',
            name='valor_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]