from .feature import Feature
from .validators import validate_point_coordinates
from ..fields import LatField, LngField


class PointBase(Feature, geom_type="Point"):
    class Meta:
        abstract = True

    def validate_coordinates(self, value):
        validate_point_coordinates(value)


class Point(PointBase):
    pass
