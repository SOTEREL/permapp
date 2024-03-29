# Generated by Django 3.2.10 on 2021-12-30 20:37

import designs.models.element_type
import designs.models.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("designs", "0011_alter_elementtype_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mapelementtype",
            name="shape_ctype",
            field=models.ForeignKey(
                limit_choices_to=designs.models.element_type.limit_shape_ctype,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="+",
                to="contenttypes.contenttype",
                validators=[designs.models.validators.validate_shape_ctype],
                verbose_name="shape type",
            ),
        ),
    ]
