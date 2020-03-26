from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .fields import LngField, LatField


class Project(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(unique=True)
    map_lng = LngField()
    map_lat = LatField()
    map_zoom = models.PositiveSmallIntegerField(
        default=settings.SATELLITE_LAYER_MAX_ZOOM
    )

    def __str__(self):
        return f"{self.name} ({self.slug})"
