# Generated by Django 4.1.3 on 2023-01-05 21:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visit', '0006_alter_visit_total_balance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moneymovement',
            old_name='category',
            new_name='categoria',
        ),
        migrations.RenameField(
            model_name='moneymovement',
            old_name='value',
            new_name='valor',
        ),
    ]