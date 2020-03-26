from django.db import models

from .polygon import PolygonBase


class Building(PolygonBase):
    roof_surface = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="m²"
    )
