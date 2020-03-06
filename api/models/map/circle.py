from django.db import models

from .point import PointBase


class CircleBase(PointBase):
    radius = models.PositiveSmallIntegerField()

    class Meta:
        abstract = True

    @property
    def geojson_props(self):
        return {**PointBase.geojson_props, "radius": self.radius}


class Circle(CircleBase):
    pass
