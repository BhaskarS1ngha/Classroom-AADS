# Generated by Django 4.1.5 on 2023-02-28 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("attendance", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attendance",
            name="status",
            field=models.BooleanField(default="False"),
        ),
        migrations.AlterField(
            model_name="attendanceclass",
            name="date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
