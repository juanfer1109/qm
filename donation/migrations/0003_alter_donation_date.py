# Generated by Django 4.1.5 on 2023-03-10 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_donation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donation',
            name='date',
            field=models.DateField(),
        ),
    ]
