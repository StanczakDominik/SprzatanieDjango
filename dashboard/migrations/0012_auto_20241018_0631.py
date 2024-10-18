# Generated by Django 5.1.1 on 2024-10-18 06:31

from django.db import migrations


def make_many(apps, schema_editor):
    Execution = apps.get_model("dashboard", "Execution")

    for execution in Execution.objects.all():
        execution.executed_by_many.add(execution.executed_by)


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0011_execution_executed_by_many_and_more"),
    ]

    operations = [migrations.RunPython(make_many)]