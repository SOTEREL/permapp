# Generated by Django 3.2.11 on 2022-01-21 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("designs", "0016_alter_elementtypecategory_options"),
    ]

    operations = [
        migrations.AlterModelOptions(name="design", options={"ordering": ["name"]},),
    ]
