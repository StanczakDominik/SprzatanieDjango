# Generated by Django 4.2.12 on 2024-09-11 12:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0004_alter_activity_date_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="execution",
            name="execution_date",
            field=models.DateTimeField(auto_now_add=True, verbose_name="date done"),
        ),
    ]
