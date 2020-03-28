from .geojson_shape import GeoJSONShape
from ..validators import validate_multipolygon_coordinates


class MultiPolygon(GeoJSONShape):
    GEOM_TYPE = "MultiPolygon"

    def validate_coordinates(self, value):
        validate_multipolygon_coordinates(value)
