# Generated by Django 4.1.3 on 2022-12-12 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_customuser_email_remove_customuser_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default=1, max_length=254, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(default=1, max_length=150),
            preserve_default=False,
        ),
    ]
