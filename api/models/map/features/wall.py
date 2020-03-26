from django.db import models

from .line import LineBase


class Wall(LineBase):
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="cm")
