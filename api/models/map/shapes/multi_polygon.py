from .geojson_shape import GeoJSONShape
from ..validators import validate_multipolygon_coordinates


class MultiPolygon(GeoJSONShape, geom_type="MultiPolygon"):
    def validate_coordinates(self, value):
        validate_multipolygon_coordinates(value)
