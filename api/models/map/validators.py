from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError

from jsonschema import Draft7Validator
from jsonschema.exceptions import SchemaError

from ..fields import LngField, LatField


def validate_feature_ctype(value):
    from .feature_type import FeatureType  # Import here to avoid circular import

    ctype = ContentType.objects.get_for_id(value)
    if ctype not in FeatureType.list_feature_ctypes():
        raise ValidationError(f"The content type '{ctype}' is not a feature type")


def validate_shape_ctype(value):
    from .feature_type import FeatureType  # Import here to avoid circular import

    ctype = ContentType.objects.get_for_id(value)
    if ctype not in FeatureType.list_shape_ctypes():
        raise ValidationError(f"The content type '{ctype}' is not a shape type")


def validate_json_schema(value):
    print("validate_json_schema", value)
    try:
        Draft7Validator.check_schema(value)
    except SchemaError as e:
        raise ValidationError(str(e))


def validate_point_coordinates(value):
    if not isinstance(value, (list, tuple)):
        raise ValidationError("Point coordinates must be a list or a tuple.")
    if len(value) != 2:
        raise ValidationError("Point can only have two coordinates.")
    lng, lat = value
    LngField().run_validators(lng)
    LatField().run_validators(lat)


def validate_line_coordinates(value):
    if not isinstance(value, (list, tuple)):
        raise ValidationError("Line coordinates must be a list or a tuple.")
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
    if not isinstance(value, (list, tuple)):
        raise ValidationError("Polygon coordinates must be a list or a tuple.")
    if len(value) != 1:
        raise ValidationError("models.map.Polygon handles single polygons only.")
    validate_linear_ring_coordinates(value[0])


def validate_multipolygon_coordinates(value):
    if not isinstance(value, (list, tuple)):
        raise ValidationError("MultiPolygon coordinates must be a list or a tuple.")
    for poly in value:
        validate_polygon_coordinates(poly)
