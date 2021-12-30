from django.contrib.contenttypes.models import ContentType
from django.db import models
from martor.models import MartorField
from polymorphic.models import PolymorphicModel
from tagging.registry import register as tagging_register

from .validators import validate_shape_ctype


def limit_shape_ctype():
    return {"pk__in": [ctype.pk for ctype in MapElementType.list_usable_shape_ctypes()]}


class ElementType(PolymorphicModel):
    name = models.CharField(max_length=50, unique=True)
    description = MartorField(default="", blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "element types"

    def __str__(self):
        return self.name


tagging_register(ElementType)


class MapElementType(ElementType):
    shape_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
        related_name="+",
        verbose_name="shape type",
        validators=[validate_shape_ctype],
        limit_choices_to=limit_shape_ctype,
    )

    class Meta(ElementType.Meta):
        verbose_name_plural = "map element types"

    @classmethod
    def list_usable_shape_ctypes(cls, as_queryset=False):
        from .map_shapes import usable_shape_models

        ctypes = ContentType.objects.get_for_models(*usable_shape_models).values()
        if as_queryset:
            return ContentType.objects.filter(pk__in=[ctype.pk for ctype in ctypes])
        return ctypes

    @property
    def shape_cls(self):
        return self.shape_ctype.model_class()

    @property
    def style_cls(self):
        return self.shape_cls.style_cls
