from django.db import models

from .point import PointBase


class PlantBase(PointBase):
    scientific_name = models.CharField(max_length=100, default="", blank=True)
    edible = models.BooleanField(null=True)

    class Meta:
        abstract = True


class Plant(PlantBase):
    pass
