# Generated by Django 4.1.3 on 2023-01-04 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moneymovement',
            name='type',
        ),
    ]
