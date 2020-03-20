from django.core.validators import MinValueValidator
from django.db import models

from .point import PointBase


class CircleBase(PointBase):
    class Meta:
        abstract = True


class Circle(CircleBase):
    pass
