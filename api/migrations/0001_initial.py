# Generated by Django 3.0.3 on 2020-04-03 17:17

import api.models.fields
import api.models.map.feature
import api.models.map.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import jsonfield.fields
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [("contenttypes", "0002_remove_content_type_name")]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("slug", models.SlugField(verbose_name="slug")),
                ("active", models.BooleanField(default=True, verbose_name="active")),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="api.Category",
                        verbose_name="parent",
                    ),
                ),
            ],
            options={"verbose_name_plural": "categories"},
            managers=[("tree", django.db.models.manager.Manager())],
        ),
        migrations.CreateModel(
            name="Feature",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_on", models.DateField(auto_now_add=True)),
                ("updated_on", models.DateField(auto_now=True)),
                ("name", models.CharField(max_length=50)),
                ("comments", models.TextField(blank=True, default="")),
                ("is_risky", models.BooleanField(default=False)),
                (
                    "permanence",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[django.core.validators.MaxValueValidator(10)],
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_api.feature_set+",
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            options={"abstract": False, "base_manager_name": "objects"},
        ),
        migrations.CreateModel(
            name="FeatureStyle",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("style", jsonfield.fields.JSONField(blank=True, default=dict)),
                (
                    "shape_ctype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.ContentType",
                        validators=[api.models.map.validators.validate_shape_ctype],
                    ),
                ),
            ],
            options={"verbose_name_plural": "feature styles"},
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("slug", models.SlugField(unique=True)),
                (
                    "map_lng",
                    api.models.fields.LngField(
                        validators=[
                            django.core.validators.MinValueValidator(-180),
                            django.core.validators.MaxValueValidator(180),
                        ]
                    ),
                ),
                (
                    "map_lat",
                    api.models.fields.LatField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(90),
                        ]
                    ),
                ),
                ("map_zoom", models.PositiveSmallIntegerField(default=19)),
            ],
        ),
        migrations.CreateModel(
            name="Shape",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "map_projection",
                    models.CharField(default="EPSG:3857", max_length=50),
                ),
                ("zoom", models.PositiveSmallIntegerField(default=19)),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "polymorphic_ctype",
                    models.ForeignKey(
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="polymorphic_api.shape_set+",
                        to="contenttypes.ContentType",
                    ),
                ),
            ],
            options={"unique_together": {("content_type", "object_id")}},
        ),
        migrations.CreateModel(
            name="View",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name="Circle",
            fields=[
                (
                    "shape_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.Shape",
                    ),
                ),
                (
                    "coordinates",
                    jsonfield.fields.JSONField(blank=True, default=None, null=True),
                ),
                (
                    "radius",
                    models.FloatField(
                        default=1,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
            ],
            options={"abstract": False},
            bases=("api.shape",),
        ),
        migrations.CreateModel(
            name="Line",
            fields=[
                (
                    "shape_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.Shape",
                    ),
                ),
                (
                    "coordinates",
                    jsonfield.fields.JSONField(blank=True, default=None, null=True),
                ),
            ],
            options={"abstract": False},
            bases=("api.shape",),
        ),
        migrations.CreateModel(
            name="MultiPolygon",
            fields=[
                (
                    "shape_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.Shape",
                    ),
                ),
                (
                    "coordinates",
                    jsonfield.fields.JSONField(blank=True, default=None, null=True),
                ),
            ],
            options={"abstract": False},
            bases=("api.shape",),
        ),
        migrations.CreateModel(
            name="Point",
            fields=[
                (
                    "shape_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.Shape",
                    ),
                ),
                (
                    "coordinates",
                    jsonfield.fields.JSONField(blank=True, default=None, null=True),
                ),
            ],
            options={"abstract": False},
            bases=("api.shape",),
        ),
        migrations.CreateModel(
            name="Polygon",
            fields=[
                (
                    "shape_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="api.Shape",
                    ),
                ),
                (
                    "coordinates",
                    jsonfield.fields.JSONField(blank=True, default=None, null=True),
                ),
            ],
            options={"abstract": False},
            bases=("api.shape",),
        ),
        migrations.CreateModel(
            name="ViewFeature",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("z_index", models.PositiveSmallIntegerField(default=0)),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.Feature"
                    ),
                ),
                (
                    "view",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.View"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="view",
            name="features",
            field=models.ManyToManyField(through="api.ViewFeature", to="api.Feature"),
        ),
        migrations.AddField(
            model_name="view",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.Project"
            ),
        ),
        migrations.CreateModel(
            name="FeatureType",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, unique=True)),
                ("slug", models.SlugField(unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.Category",
                    ),
                ),
                (
                    "shape_ctype",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="contenttypes.ContentType",
                        validators=[api.models.map.validators.validate_shape_ctype],
                    ),
                ),
                (
                    "style",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="api.FeatureStyle",
                    ),
                ),
            ],
            options={"verbose_name_plural": "feature types"},
        ),
        migrations.CreateModel(
            name="FeatureAttachment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "upload",
                    models.FileField(upload_to=api.models.map.feature.attachment_path),
                ),
                ("comments", models.TextField(blank=True, default="")),
                (
                    "feature",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attachments",
                        to="api.Feature",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="feature",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.Project"
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="api.FeatureType"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="view", unique_together={("project", "name")}
        ),
    ]
