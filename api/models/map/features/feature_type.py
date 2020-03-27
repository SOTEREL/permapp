from django.db import models
from django.utils.text import slugify

from jsonfield import JSONField

from ..category import Category
from ..validators import validate_json_schema


class FeatureType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    extra_props_schema = JSONField(
        default=None, null=True, blank=True, validators=[validate_json_schema]
    )

    class Meta:
        verbose_name_plural = "feature types"

    def __str__(self):
        return self.name
