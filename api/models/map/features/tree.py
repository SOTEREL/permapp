from django.db import models

from .plant import PlantBase


class Tree(PlantBase):
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="m")
    persistent = models.BooleanField(null=True)
