from .feature import Feature
from ..validators import validate_polygon_coordinates, validate_multipolygon_coordinates


class PolygonBase(Feature, geom_type="Polygon"):
    class Meta:
        abstract = True

    def validate_coordinates(self, value):
        validate_polygon_coordinates(value)


class MultiPolygonBase(PolygonBase, geom_type="MultiPolygon"):
    class Meta:
        abstract = True

    def validate_coordinates(self, value):
        validate_multipolygon_coordinates(value)


class Polygon(PolygonBase, is_generic=True):
    pass


class MultiPolygon(MultiPolygonBase, is_generic=True):
    pass
