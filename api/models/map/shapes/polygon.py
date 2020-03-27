from .geojson_shape import GeoJSONShape
from ..validators import validate_polygon_coordinates


class Polygon(GeoJSONShape, geom_type="Polygon"):
    def validate_coordinates(self, value):
        validate_polygon_coordinates(value)
