# Generated by Django 5.1.1 on 2024-10-01 15:40

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [
        ("dashboard", "0001_initial"),
        ("dashboard", "0002_alter_activity_date_created"),
        ("dashboard", "0003_alter_activity_date_created"),
        ("dashboard", "0004_alter_activity_date_created"),
        ("dashboard", "0005_alter_execution_execution_date"),
        ("dashboard", "0006_alter_execution_executed_by_delete_participant"),
        ("dashboard", "0007_alter_execution_activity"),
        ("dashboard", "0008_alter_execution_activity_alter_execution_executed_by"),
        ("dashboard", "0009_alter_activity_date_created_and_more"),
    ]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Activity",
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
                ("activity_name", models.CharField(max_length=200)),
                (
                    "date_created",
                    models.DateField(
                        default=datetime.date.today, verbose_name="date created"
                    ),
                ),
                (
                    "expected_period",
                    models.DurationField(verbose_name="expected period"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Execution",
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
                (
                    "execution_date",
                    models.DateField(
                        default=datetime.date.today, verbose_name="date done"
                    ),
                ),
                (
                    "activity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="dashboard.activity",
                    ),
                ),
                (
                    "executed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
