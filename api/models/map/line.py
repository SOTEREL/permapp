from .feature import Feature
from .validators import validate_line_coordinates


class LineBase(Feature, geom_type="LineString"):
    class Meta:
        abstract = True

    def validate_coordinates(self, value):
        validate_line_coordinates(value)


class Line(LineBase):
    pass
