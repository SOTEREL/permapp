from django.db import models

from .point import Point


class Circle(Point):
    radius = models.PositiveSmallIntegerField()

    @property
    def geojson_props(self):
        return {"radius": self.radius}
