# Generated by Django 5.0 on 2024-12-07 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("task_management", "0006_dailykeywordselection"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="task_management.taskcategory",
            ),
        ),
    ]
