# Generated by Django 4.1.4 on 2023-02-12 00:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0014_customuser_staff"),
        ("visit", "0008_visit_revisado"),
    ]

    operations = [
        migrations.CreateModel(
            name="VisitCalendar",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                (
                    "visitor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="users.customuser",
                    ),
                ),
            ],
        ),
    ]