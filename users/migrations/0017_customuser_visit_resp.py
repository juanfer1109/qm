# Generated by Django 4.1.5 on 2023-04-19 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_customuser_donations'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='visit_resp',
            field=models.BooleanField(default=False),
        ),
    ]
