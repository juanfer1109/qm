# Generated by Django 4.1.5 on 2023-04-24 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0015_inscripciones_valor_recibido_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripciones',
            name='comentarios',
            field=models.TextField(blank=True, null=True),
        ),
    ]
