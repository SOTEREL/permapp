from django.db import models

from .feature import Feature


class Building(Feature):
    roof_surface = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="m²"
    )
