from django.db import models

from .line import LineBase


class Hedge(LineBase):
    height = models.PositiveSmallIntegerField(null=True, blank=True, help_text="m")
