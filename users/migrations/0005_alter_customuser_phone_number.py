# Generated by Django 4.1.3 on 2022-12-19 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_customuser_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.PositiveBigIntegerField(),
        ),
    ]
