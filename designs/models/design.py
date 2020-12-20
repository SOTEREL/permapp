from django.conf import settings
from django.db import models
from djgeojson.fields import PointField


class Design(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    map_center = PointField()
    map_zoom = models.PositiveSmallIntegerField(
        default=settings.SATELLITE_LAYER_MAX_ZOOM
    )

    def __str__(self):
        return self.name
