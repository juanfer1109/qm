# Generated by Django 4.1.3 on 2023-01-15 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0008_evento_prueba'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='tipo',
            field=models.CharField(choices=[('Taller', 'Taller'), ('Encuentro', 'Encuentro'), ('Experiencia', 'Experiencia')], max_length=15),
        ),
    ]
