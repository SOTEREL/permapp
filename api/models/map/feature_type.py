from django.db import models
from django.utils.text import slugify

from jsonfield import JSONField

from .category import Category
from .shapes import SHAPE_MODEL_NAMES
from .validators import validate_json_schema

shape_model_choices = [(x, x) for x in SHAPE_MODEL_NAMES]


class FeatureType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    shape_model = models.CharField(max_length=70, choices=shape_model_choices)
    extra_props_schema = JSONField(
        default=None, null=True, blank=True, validators=[validate_json_schema]
    )

    class Meta:
        verbose_name_plural = "feature types"

    def __str__(self):
        return self.name
