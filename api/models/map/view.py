from django.conf import settings
from django.db import models

from .feature import Feature
from ..project import Project


class View(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    features = models.ManyToManyField(
        Feature, through="ViewFeature", through_fields=("view", "feature")
    )

    class Meta:
        unique_together = ("project", "name")

    def __str__(self):
        return self.name


class ViewTileLayer(models.Model):
    NAME_CHOICES = [(name, name) for name in settings.MAP_TILE_LAYERS]
    view = models.ForeignKey(View, on_delete=models.CASCADE, related_name="tile_layers")
    name = models.CharField(max_length=100, choices=NAME_CHOICES)

    class Meta:
        unique_together = ("view", "name")

    def __str__(self):
        return self.name


class ViewFeature(models.Model):
    view = models.ForeignKey(View, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)
