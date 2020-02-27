from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()
    map_lng = models.FloatField(
        validators=[MinValueValidator(-180), MaxValueValidator(180)]
    )
    map_lat = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(90)]
    )
    map_zoom = models.PositiveSmallIntegerField(default=19)

    def __str__(self):
        return f"{self.name} ({self.id})"
