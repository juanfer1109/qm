# Generated by Django 4.1.3 on 2022-12-18 00:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boletin', '0002_article_author_alter_issue_release_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='image',
            field=models.ImageField(default=1, upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='issue',
            name='release_date',
            field=models.DateField(default=datetime.datetime(2022, 12, 17, 19, 23, 13, 885333)),
        ),
    ]