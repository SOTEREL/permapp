from django.db import models
from solo.models import SingletonModel

from .map_theme import MapTheme


class Configuration(SingletonModel):
    default_map_theme = models.ForeignKey(MapTheme, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "global configuration"

    def __str__(self):
        return "Global configuration"
