from django.db import models

from ..project import Project


# TODO:
# * add projection field
# * add properties for area and length
# * add style field
class Feature(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default="", blank=True)
    description = models.TextField(default="", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name or self.id

    @property
    def center(self):
        raise NotImplementedError()

    @property
    def geojson_geom(self):
        raise NotImplementedError()

    @property
    def geojson_props(self):
        return {}

    @property
    def geojson(self):
        return {
            "type": "Feature",
            "geometry": self.geojson_geom,
            "properties": self.geojson_props,
        }
