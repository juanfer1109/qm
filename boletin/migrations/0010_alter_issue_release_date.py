# Generated by Django 4.1.3 on 2023-01-02 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boletin', '0009_alter_issue_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2023, 1, 2, 12, 23, 9, 575591)),
        ),
    ]