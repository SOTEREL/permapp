from django.db import models
from jsonfield import JSONField
from shapely.geometry import shape

from .shape import Shape


class GeoJSONShape(Shape):
    coordinates = JSONField(default=None, null=True, blank=True)

    class Meta:
        abstract = True

    def __init_subclass__(cls, *, geom_type, **kwargs):
        cls.geom_type = geom_type

    def validate_coordinates(self, value):
        raise NotImplementedError(
            f"{self.__class__.__name__}.validate_coordinates() must be implemented"
        )

    def clean(self):
        super().clean()
        self.validate_coordinates(self.coordinates)

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
        return {"type": self.geom_type, "coordinates": self.coordinates}

    @property
    def geojson_props(self):
        return {"id": self.id, "name": self.name, "projection": self.map_projection}

    @property
    def geojson(self):
        return {
            "type": "Feature",
            "geometry": self.geojson_geom,
            "properties": self.geojson_props,
        }
