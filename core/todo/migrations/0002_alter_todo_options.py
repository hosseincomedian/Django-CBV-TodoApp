# Generated by Django 4.2.2 on 2023-06-18 11:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="todo",
            options={"ordering": ("-created_time",)},
        ),
    ]
