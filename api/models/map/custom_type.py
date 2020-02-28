from django.db import models

from .category import Category
from ..project import Project


class CustomType(models.Model):
    project = models.ForeignKey(
        Project, related_name="custom_map_types", on_delete=models.CASCADE
    )
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
