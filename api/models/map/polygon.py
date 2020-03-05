from django.core.exceptions import ValidationError

from jsonfield import JSONField

from .feature import Feature
from .line import validate_coordinates as validate_line_coordinates
from ..fields import LatField, LngField


def validate_linear_ring_coordinates(value):
    validate_line_coordinates(value)
    if len(value) < 4:
        raise ValidationError("Linear ring must have 4 points or more.")
    first, *_, last = value
    if first[0] != last[0] or first[1] != last[1]:
        raise ValidationError(
            "First and last coordinates of linear rings must be identical."
        )


def validate_polygon_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("Polygon coordinates must be a list.")
    if len(value) != 1:
        raise ValidationError("models.map.Polygon handles single polygons only.")
    validate_linear_ring_coordinates(value[0])


def validate_multipolygon_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("MultiPolygon coordinates must be a list.")
    for poly in value:
        validate_polygon_coordinates(poly)


class PolygonBase(Feature):
    coordinates = JSONField(validators=[validate_polygon_coordinates])

    class Meta:
        abstract = True

    @property
    def center(self):
        raise NotImplementedError()

    @property
    def geojson_geom(self):
        return {"type": "Polygon", "coordinates": self.coordinates}


class Polygon(PolygonBase):
    pass


class MultiPolygonBase(PolygonBase):
    coordinates = JSONField(validators=[validate_multipolygon_coordinates])

    class Meta:
        abstract = True

    @property
    def center(self):
        raise NotImplementedError()

    @property
    def geojson_geom(self):
        return {"type": "MultiPolygon", "coordinates": self.coordinates}


class MultiPolygon(MultiPolygonBase):
    pass
