from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from polymorphic.models import PolymorphicModel


usable_shape_models = []


class Shape(PolymorphicModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    element = GenericForeignKey("content_type", "object_id")
    map_projection = models.CharField(
        max_length=50, default=settings.LEAFLET_DEFAULT_PROJECTION
    )
    edit_zoom = models.PositiveSmallIntegerField(
        default=settings.SATELLITE_LAYER_MAX_ZOOM
    )

    class Meta:
        unique_together = ("content_type", "object_id")

    def __init_subclass__(cls, *, style_cls, usable=True, **kwargs):
        cls.style_cls = style_cls
        if usable:
            usable_shape_models.append(cls)

    def __str__(self):
        return f"{self.__class__.__name__} of {self.element}"

    @property
    def is_drawable(self):
        raise NotImplementedError(
            f"{self.__class__.__name__}.is_drawable property must be implemented"
        )

    @property
    def centroid(self):
        raise NotImplementedError(
            f"{self.__class__.__name__}.centroid property must be implemented"
        )
