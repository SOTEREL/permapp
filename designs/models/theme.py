from django.db import models

from .element_type import MapElementType


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def missing_map_element_types(self):
        pks = list(self.styles.values_list("map_element_type__pk", flat=True))
        return MapElementType.objects.exclude(pk__in=pks)
