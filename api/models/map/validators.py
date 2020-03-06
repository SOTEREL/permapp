from django.core.exceptions import ValidationError

from ..fields import LngField, LatField


def validate_point_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("Point coordinates must be a list.")
    if len(value) != 2:
        raise ValidationError("Point can only have two coordinates.")
    lng, lat = value
    LngField().run_validators(lng)
    LatField().run_validators(lat)


def validate_line_coordinates(value):
    if not isinstance(value, list):
        raise ValidationError("Line coordinates must be a list.")
    if len(value) < 2:
        raise ValidationError("Line coordinates must contain at least two points.")
    for p in value:
        validate_point_coordinates(p)


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
