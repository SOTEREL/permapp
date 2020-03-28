from .geojson_shape import GeoJSONShape
from ..validators import validate_line_coordinates


class Line(GeoJSONShape):
    GEOM_TYPE = "LineString"

    def validate_coordinates(self, value):
        validate_line_coordinates(value)
