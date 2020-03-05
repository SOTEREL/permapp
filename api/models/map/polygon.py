from django.core.exceptions import ValidationError

from jsonfield import JSONField

from .feature import Feature
from ..fields import LatField, LngField


def validate_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("Polygon coordinates must be a list.")
    if len(value) != 1:
        raise ValidationError("models.map.Polygon handles single polygons only.")
    if len(value[0]) < 3:
        raise ValidationError("Coordinates must contain at least three points.")
    first, *_, last = value[0]
    if first[0] != last[0] or first[1] != last[1]:
        raise ValidationError("First and last coordinates must be identical.")


class Polygon(Feature):
    coordinates = JSONField(validators=[validate_coordinates])

    @property
    def center(self):
        return dict(lat=self.lat, lng=self.lng)

    @property
    def geojson_geom(self):
        return {"type": "Polygon", "coordinates": self.coordinates}
