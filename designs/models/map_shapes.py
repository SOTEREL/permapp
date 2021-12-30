from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from djgeojson.fields import (
    GeometryCollectionField,
    LineStringField,
    MultiPolygonField,
    PointField,
    PolygonField,
)
from polymorphic.models import PolymorphicModel
from shapely.geometry import shape

from .element import MapElement
from .map_styles import CircleStyle, LineStyle, PointStyle, PolygonStyle

usable_shape_models = []


class Shape(PolymorphicModel):
    map_element = models.OneToOneField(
        MapElement, on_delete=models.CASCADE, related_name="shape"
    )
    map_projection = models.CharField(
        max_length=50, default=settings.LEAFLET_DEFAULT_PROJECTION
    )
    edit_zoom = models.PositiveSmallIntegerField(
        default=settings.DEFAULT_SHAPE_EDIT_ZOOM
    )

    def __init_subclass__(cls, *, style_cls, usable=True, **kwargs):
        cls.style_cls = style_cls
        if usable:
            usable_shape_models.append(cls)

    def __str__(self):
        return f"{self.__class__.__name__} of {self.map_element}"

    @property
    def is_drawable(self):
        raise NotImplementedError(
            f"{self.__class__.__name__}.is_drawable property must be implemented"
        )

    @property
    def centroid(self):
        raise NotImplementedError(
            f"{self.__class__.__name__}.centroid property must be implemented"
        )


class GeoJSONShape(Shape, style_cls=None, usable=False):
    geom = None

    class Meta:
        abstract = True

    @property
    def is_drawable(self):
        return bool(self.geom)

    @property
    def centroid(self):
        return shape(self.geom).centroid

    @property
    def perimeter(self):
        return shape(self.geom).length

    @property
    def area(self):
        return shape(self.geom).area

    @property
    def geojson(self):
        if not self.is_drawable:
            return None
        return {
            "type": "Feature",
            "geometry": self.geom,
            "properties": {},
        }


class Circle(GeoJSONShape, style_cls=CircleStyle):
    geom = PointField()
    radius = models.FloatField(default=1, validators=[MinValueValidator(0)])


class Line(GeoJSONShape, style_cls=LineStyle):
    geom = LineStringField()


class MultiPolygon(GeoJSONShape, style_cls=PolygonStyle):
    geom = MultiPolygonField()


class Point(GeoJSONShape, style_cls=PointStyle):
    geom = PointField()


class Polygon(GeoJSONShape, style_cls=PolygonStyle):
    geom = PolygonField()


class Geometry(GeoJSONShape, style_cls=PolygonStyle):
    geom = GeometryCollectionField()
