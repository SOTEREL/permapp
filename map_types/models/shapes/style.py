from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from ..validators import validate_dash_array


class ShapeStyle(PolymorphicModel):
    pass


class AbstractLineStyle(models.Model):
    color = ColorField()
    weight = models.PositiveSmallIntegerField()
    opacity = models.PositiveSmallIntegerField(
        default=100, validators=[MaxValueValidator(100)]
    )
    dash_array = models.CharField(max_length=50, validators=[validate_dash_array])

    class Meta:
        abstract = True


class LineStyle(AbstractLineStyle, ShapeStyle):
    pass


class AbstractPointStyle(models.Model):
    icon = models.ImageField()

    class Meta:
        abstract = True


class PointStyle(AbstractPointStyle, ShapeStyle):
    pass


class PolygonStyle(AbstractLineStyle, ShapeStyle):
    fill_color = ColorField()
    fill_opacity = models.PositiveSmallIntegerField(
        default=100, validators=[MaxValueValidator(100)]
    )


class CircleStyle(AbstractLineStyle, AbstractPointStyle, ShapeStyle):
    pass
