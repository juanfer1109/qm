# Generated by Django 4.1.3 on 2022-12-30 01:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boletin', '0008_alter_issue_release_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 29, 20, 27, 24, 752225)),
        ),
    ]
