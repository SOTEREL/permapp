# Generated by Django 3.0.3 on 2020-03-28 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("api", "0002_auto_20200328_1728")]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.FeatureType",
            ),
            preserve_default=False,
        )
    ]