# Generated by Django 4.1.5 on 2023-03-10 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]