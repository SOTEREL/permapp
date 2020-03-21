from django.db import models

from .line import LineBase


class Pathway(LineBase):
    is_road = models.BooleanField(null=True)
