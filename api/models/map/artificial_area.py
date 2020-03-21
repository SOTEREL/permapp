from django.db import models

from .polygon import MultiPolygonBase


class ArtificialArea(MultiPolygonBase):
    surface = models.PositiveSmallIntegerField(null=True, blank=True, help_text="m²")
