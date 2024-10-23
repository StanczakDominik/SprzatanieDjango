# Generated by Django 5.1.1 on 2024-10-23 11:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0015_alter_execution_executed_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="activity",
            name="notes",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="Notes or description of the activity",
            ),
        ),
    ]
