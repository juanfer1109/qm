# Generated by Django 4.1.3 on 2023-01-04 12:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0009_customuser_mtto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField()),
                ('total_balance', models.BigIntegerField()),
                ('visitor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='MoneyMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Ingreso', 'Ingreso'), ('Egreso', 'Egreso')], default='Ingreso', max_length=7)),
                ('value', models.PositiveBigIntegerField()),
                ('visit', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mtto.visit')),
            ],
            options={
                'ordering': ['visit'],
            },
        ),
    ]
