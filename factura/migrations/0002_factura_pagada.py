# Generated by Django 4.2.4 on 2023-08-26 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='pagada',
            field=models.BooleanField(default=False),
        ),
    ]
