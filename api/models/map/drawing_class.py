from django.db import models


class DrawingClass(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "drawing classes"

    def __str__(self):
        return self.name
