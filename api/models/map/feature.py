from django.db import models
from jsonfield import JSONField

from ..project import Project


class Feature(models.Model):
    project = models.ForeignKey(
        Project, related_name="features", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    description = models.TextField(default="", blank=True)
    geom = JSONField(null=True, blank=True)

    def __str__(self):
        return self.name
