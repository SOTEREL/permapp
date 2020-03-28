from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from jsonfield import JSONField

from polymorphic.models import PolymorphicModel

from shapely.geometry import shape

from ..feature import Feature


class Shape(PolymorphicModel):
    feature = models.OneToOneField(Feature, on_delete=models.CASCADE)
    map_projection = models.CharField(
        max_length=50, default=settings.LEAFLET_DEFAULT_PROJECTION
    )

    def __str__(self):
        return str(self.feature)

    @property
    def centroid(self):
        raise NotImplementedError(
            f"{self.__class__.__name__}.centroid property must be implemented"
        )
