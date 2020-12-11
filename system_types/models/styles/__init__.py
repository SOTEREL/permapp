from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from ..theme import ThemedElementType
from ..validators import validate_dash_array


class ElementTypeStyle(PolymorphicModel):
    themed_element_type = models.OneToOneField(
        ThemedElementType, on_delete=models.CASCADE, related_name="style"
    )

    def __str__(self):
        return f"{self.__class__.__name__} of {self.themed_element_type}"


class AbstractLineStyle(models.Model):
    color = ColorField()
    weight = models.PositiveSmallIntegerField(default=2)
    opacity = models.PositiveSmallIntegerField(
        default=100, validators=[MaxValueValidator(100)]
    )
    dash_array = models.CharField(
        max_length=50,
        blank=True,
        validators=[validate_dash_array],
        help_text="Example: 5-5",
    )

    class Meta:
        abstract = True


class LineStyle(AbstractLineStyle, ElementTypeStyle):
    pass


class AbstractPointStyle(models.Model):
    icon = models.ImageField(null=True)

    class Meta:
        abstract = True


class PointStyle(AbstractPointStyle, ElementTypeStyle):
    pass


class PolygonStyle(AbstractLineStyle, ElementTypeStyle):
    fill_color = ColorField()
    fill_opacity = models.PositiveSmallIntegerField(
        default=100, validators=[MaxValueValidator(100)]
    )


class CircleStyle(AbstractLineStyle, AbstractPointStyle, ElementTypeStyle):
    pass
