# Generated by Django 4.1.5 on 2023-01-26 00:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0013_evento_duracion_evento_incluye_evento_lugar'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripciones',
            name='cantidad',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]