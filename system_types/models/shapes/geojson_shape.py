from django.core.validators import MinValueValidator
from django.db import models
from jsonfield import JSONField
from shapely.geometry import shape

from .shape import Shape
from .style import CircleStyle, LineStyle, PointStyle, PolygonStyle
from ..validators import (
    validate_line_coordinates,
    validate_point_coordinates,
    validate_multipolygon_coordinates,
    validate_polygon_coordinates,
)


class GeoJSONShape(Shape, style_cls=None):
    coordinates = JSONField(default=None, null=True, blank=True)

    class Meta:
        abstract = True

    def __init_subclass__(cls, *, geom_type, validate_coordinates, **kwargs):
        cls.geom_type = geom_type
        cls.validate_coordinates = validate_coordinates
        super().__init_subclass__(**kwargs)

    def clean_fields(self, exclude=None):
        super().clean_fields(exclude=exclude)
        if self.coordinates is not None and (
            not exclude or "coordinates" not in exclude
        ):
            self.validate_coordinates(self.coordinates)

    @property
    def is_drawable(self):
        return self.coordinates is not None

    @property
    def centroid(self):
        return shape(self.geojson_geom).centroid

    @property
    def perimeter(self):
        return shape(self.geojson_geom).length

    @property
    def area(self):
        return shape(self.geojson_geom).area

    @property
    def geojson_geom(self):
        return {"type": self.GEOM_TYPE, "coordinates": self.coordinates}

    @property
    def geojson_props(self):
        return {"id": self.id, "projection": self.map_projection}

    @property
    def geojson(self):
        return {
            "type": "Feature",
            "geometry": self.geojson_geom,
            "properties": self.geojson_props,
        }


class Circle(
    GeoJSONShape,
    style_cls=CircleStyle,
    geom_type="Point",
    validate_coordinates=validate_point_coordinates,
):
    radius = models.FloatField(default=1, validators=[MinValueValidator(0)])


class Line(
    GeoJSONShape,
    style_cls=LineStyle,
    geom_type="LineString",
    validate_coordinates=validate_line_coordinates,
):
    pass


class MultiPolygon(
    GeoJSONShape,
    style_cls=PolygonStyle,
    geom_type="MultiPolygon",
    validate_coordinates=validate_multipolygon_coordinates,
):
    pass


class Point(
    GeoJSONShape,
    style_cls=PointStyle,
    geom_type="Point",
    validate_coordinates=validate_point_coordinates,
):
    pass


class Polygon(
    GeoJSONShape,
    style_cls=PolygonStyle,
    geom_type="Polygon",
    validate_coordinates=validate_polygon_coordinates,
):
    pass
