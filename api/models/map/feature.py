from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from jsonfield import JSONField

from shapely.geometry import shape

from .category import Category
from ..project import Project


class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    coordinates = JSONField()
    map_projection = models.CharField(
        max_length=50, default=settings.LEAFLET_DEFAULT_PROJECTION
    )
    style = JSONField(default=dict, blank=True)
    is_risky = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category, null=True, blank=True, on_delete=models.SET_NULL
    )
    permanence = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(settings.FEATURE_PERMANENCE_MAX)],
    )

    def __init_subclass__(cls, *, geom_type=None, **kwargs):
        # geom_type is only defined for abstract shape classes
        if geom_type is not None:
            cls.geom_type = geom_type

    def __str__(self):
        return self.name

    def validate_coordinates(self, value):
        raise NotImplementedError(
            f"{self.__class__.__name__}.validate_coordinates() must be implemented"
        )

    def clean(self):
        super().clean()
        self.validate_coordinates(self.coordinates)

    @property
    def centroid(self):
        return shape(self.geojson_geom).centroid

    @property
    def perimeter(self):
        return shape(self.geojson_geom).length

    @property
    def area(self):
        return shape(self.geojson_geom).area

    @property
    def geojson_geom(self):
        return {"type": self.geometry_type, "coordinates": self.coordinates}

    @property
    def geojson_props(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "style": self.style,
            "projection": self.projection,
        }

    @property
    def geojson(self):
        return {
            "type": "Feature",
            "geometry": self.geojson_geom,
            "properties": self.geojson_props,
        }
