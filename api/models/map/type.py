from django.db import models

from .category import Category


class Type(models.Model):
    slug = models.SlugField(primary_key=True)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(
        Category, related_name="types", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name
