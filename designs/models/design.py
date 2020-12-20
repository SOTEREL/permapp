from django.conf import settings
from django.db import models
from djgeojson.fields import PointField

from .configuration import Configuration
from .theme import Theme


def get_default_theme():
    theme = Configuration.get_solo().default_theme
    if theme is None:
        return None
    return theme.pk


class Design(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    map_center = PointField()
    map_zoom = models.PositiveSmallIntegerField(default=settings.DEFAULT_PROJECT_ZOOM)
    theme = models.ForeignKey(
        Theme, default=get_default_theme, null=True, on_delete=models.SET_DEFAULT
    )

    def __str__(self):
        return self.name
