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


class ViewFeature(models.Model):
    view = models.ForeignKey(View, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    z_index = models.PositiveSmallIntegerField(default=0)
    min_zoom = models.PositiveSmallIntegerField(default=0)
    max_zoom = models.PositiveSmallIntegerField(null=True, blank=True)
