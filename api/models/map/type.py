from django.db import models

from .category import Category
from ..project import Project


class Type(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class CustomType(Type):
    project = models.ForeignKey(
        Project, related_name="custom_map_types", on_delete=models.CASCADE
    )
