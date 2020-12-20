from django.db import models
from solo.models import SingletonModel

from .theme import Theme


class Configuration(SingletonModel):
    default_theme = models.ForeignKey(Theme, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = "site configuration"

    def __str__(self):
        return "Site configuration"
