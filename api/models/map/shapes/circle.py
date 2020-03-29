from django.core.validators import MinValueValidator
from django.db import models

from .geojson_shape import GeoJSONShape
from ..validators import validate_point_coordinates


class Circle(GeoJSONShape):
    GEOM_TYPE = "Point"

    radius = models.FloatField(default=1, validators=[MinValueValidator(0)])

    def validate_coordinates(self, value):
        validate_point_coordinates(value)
