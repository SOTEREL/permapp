from .geojson_shape import GeoJSONShape
from ..validators import validate_point_coordinates


class Point(GeoJSONShape, geom_type="Point"):
    def validate_coordinates(self, value):
        validate_point_coordinates(value)
