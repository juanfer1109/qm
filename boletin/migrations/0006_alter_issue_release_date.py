# Generated by Django 4.1.3 on 2022-12-19 02:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boletin', '0005_alter_article_options_alter_article_author_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 18, 21, 12, 4, 945065)),
        ),
    ]
