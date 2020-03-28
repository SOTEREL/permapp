from .geojson_shape import GeoJSONShape
from ..validators import validate_point_coordinates


class Point(GeoJSONShape):
    GEOM_TYPE = "Point"
    STYLE_SCHEMA = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "iconUrl": {"type": "string"},
            "iconSize": {
                "type": "array",
                "items": [{"type": "number"}, {"type": "number"}],
                "additionalItems": False,
            },
            "iconAnchor": {
                "type": "array",
                "items": [{"type": "number"}, {"type": "number"}],
                "additionalItems": False,
            },
            "popupAnchor": {
                "type": "array",
                "items": [{"type": "number"}, {"type": "number"}],
                "additionalItems": False,
            },
            "shadowUrl": {"type": "string"},
            "shadowSize": {
                "type": "array",
                "items": [{"type": "number"}, {"type": "number"}],
                "additionalItems": False,
            },
            "shadowAnchor": {
                "type": "array",
                "items": [{"type": "number"}, {"type": "number"}],
                "additionalItems": False,
            },
        },
        "additionalProperties": False,
    }

    def validate_coordinates(self, value):
        validate_point_coordinates(value)
