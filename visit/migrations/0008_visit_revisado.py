# Generated by Django 4.1.3 on 2023-01-06 03:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0007_rename_category_moneymovement_categoria_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='revisado',
            field=models.BooleanField(default=False),
        ),
    ]