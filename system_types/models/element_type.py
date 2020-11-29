from django.db import models
from tagging.registry import register as tagging_register


class ElementType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="", blank=True)
    needs = models.TextField(default="", blank=True)
    contributions = models.TextField(default="", blank=True)

    class Meta:
        verbose_name_plural = "element types"


tagging_register(ElementType)
