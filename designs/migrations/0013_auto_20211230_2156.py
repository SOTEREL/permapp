# Generated by Django 3.2.10 on 2021-12-30 20:56

from django.db import migrations, models
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ("designs", "0012_alter_mapelementtype_shape_ctype"),
    ]

    operations = [
        migrations.RemoveField(model_name="element", name="contributions",),
        migrations.RemoveField(model_name="element", name="needs",),
        migrations.AlterField(
            model_name="element",
            name="description",
            field=martor.models.MartorField(blank=True, default=""),
        ),
        migrations.AlterField(
            model_name="element",
            name="observation_date",
            field=models.DateField(
                blank=True,
                help_text="If empty, an unexisting element (to be added).",
                null=True,
            ),
        ),
    ]