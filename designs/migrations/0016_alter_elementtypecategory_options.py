# Generated by Django 3.2.10 on 2022-01-06 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("designs", "0015_alter_configuration_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="elementtypecategory",
            options={
                "verbose_name": "element type category",
                "verbose_name_plural": "element type categories",
            },
        ),
    ]
