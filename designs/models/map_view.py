from django.db import models

from .design import Design
from .element import MapElement


class MapView(models.Model):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)

    class Meta:
        unique_together = ("design", "name")

    def __str__(self):
        return self.name

    @property
    def ordered_elements(self):
        return self.elements.order_by("z_index")


class MapViewElement(models.Model):
    view = models.ForeignKey(MapView, on_delete=models.CASCADE, related_name="elements")
    map_element = models.ForeignKey(MapElement, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)
    min_zoom = models.PositiveSmallIntegerField(default=0)
    max_zoom = models.PositiveSmallIntegerField(null=True, blank=True)
