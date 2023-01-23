# Generated by Django 4.1.3 on 2023-01-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0010_rename_costo_evento_costo1_evento_costo2_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='costo',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='evento',
            name='fecha_costo',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]