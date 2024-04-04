# Generated by Django 5.0.3 on 2024-04-04 05:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name="Mobile",
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
                ("Name", models.CharField(max_length=20)),
                ("Price", models.PositiveSmallIntegerField()),
                ("img", models.ImageField(upload_to="images/")),
                ("Description", models.TextField()),
                ("RAM", models.CharField(max_length=10)),
                ("Camera", models.CharField(max_length=25)),
                ("Display", models.CharField(max_length=10)),
                ("OS", models.CharField(max_length=30)),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.company"
                    ),
                ),
            ],
        ),
    ]
