# Generated by Django 4.1.3 on 2023-01-17 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtto', '0005_alter_equip_last_maintenance_alter_equip_last_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='phone_number',
            field=models.PositiveBigIntegerField(),
        ),
    ]
