# Generated by Django 3.2.10 on 2021-12-30 20:25

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ("designs", "0010_auto_20211230_2122"),
    ]

    operations = [
        migrations.AlterField(
            model_name="elementtype",
            name="description",
            field=martor.models.MartorField(blank=True, default=""),
        ),
    ]
