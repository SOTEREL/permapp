from django.conf import settings
from django.db import models
from djgeojson.fields import PointField

from .configuration import Configuration
from .map_theme import MapTheme


def get_default_map_theme():
    map_theme = Configuration.get_solo().default_map_theme
    if map_theme is None:
        return None
    return map_theme.pk


class Design(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    map_center = PointField()
    map_zoom = models.PositiveSmallIntegerField(default=settings.DEFAULT_PROJECT_ZOOM)
    map_theme = models.ForeignKey(
        MapTheme, default=get_default_map_theme, null=True, on_delete=models.SET_DEFAULT
    )

    def __str__(self):
        return self.name
