from django.core.exceptions import ValidationError

from jsonfield import JSONField

from .feature import Feature
from ..fields import LatField, LngField


def validate_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("Line coordinates must be a list.")
    if len(value) < 2:
        raise ValidationError("Coordinates must contain at least two points.")


class LineBase(Feature):
    coordinates = JSONField(validators=[validate_coordinates])

    class Meta:
        abstract = True

    @property
    def center(self):
        return dict(lat=self.lat, lng=self.lng)

    @property
    def geojson_geom(self):
        return {"type": "LineString", "coordinates": self.coordinates}


class Line(LineBase):
    pass
