from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from .element_type import MapElementType
from .theme import Theme
from .validators import validate_dash_array


class MapElementTypeStyle(PolymorphicModel):
    map_element_type = models.ForeignKey(
        MapElementType, on_delete=models.CASCADE, related_name="styles"
    )
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name="styles")

    class Meta:
        verbose_name = "style of map element type"
        verbose_name_plural = "styles of map element types"
        ordering = ["theme", "map_element_type"]

    def __str__(self):
        return f'Style of "{self.map_element_type.name}" in theme "{self.theme.name}"'


class AbstractLineStyle(models.Model):
    color = ColorField(help_text="A valid CSS color.")
    weight = models.PositiveSmallIntegerField(default=2)
    opacity = models.PositiveSmallIntegerField(
        default=100, verbose_name="opacity (%)", validators=[MaxValueValidator(100)]
    )
    dash_array = models.CharField(
        max_length=50,
        blank=True,
        validators=[validate_dash_array],
        help_text="Example: 5-5",
    )

    class Meta:
        abstract = True


class LineStyle(AbstractLineStyle, MapElementTypeStyle):
    pass


class AbstractPointStyle(models.Model):
    icon = models.ImageField(null=True)

    class Meta:
        abstract = True


class PointStyle(AbstractPointStyle, MapElementTypeStyle):
    pass


class PolygonStyle(AbstractLineStyle, MapElementTypeStyle):
    fill_color = ColorField(help_text="A valid CSS color.")
    fill_opacity = models.PositiveSmallIntegerField(
        default=100,
        verbose_name="fill opacity (%)",
        validators=[MaxValueValidator(100)],
    )


class CircleStyle(AbstractLineStyle, AbstractPointStyle, MapElementTypeStyle):
    pass
