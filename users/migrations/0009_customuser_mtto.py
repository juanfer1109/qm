# Generated by Django 4.1.3 on 2023-01-04 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_customuser_tiene_reclamacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='mtto',
            field=models.BooleanField(default=False),
        ),
    ]
