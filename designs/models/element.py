from django.db import models
from polymorphic.models import PolymorphicModel
from tagging.registry import register as tagging_register

from .element_type import ElementType


class Element(PolymorphicModel):
    element_type = models.ForeignKey(ElementType, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="", blank=True)
    needs = models.TextField(default="", blank=True)
    contributions = models.TextField(default="", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


tagging_register(Element)


class MapElement(Element):
    pass
