from django.db import models

from .element_type import ElementType


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def missing_element_types(self):
        # TODO
        pks = list(self.element_types.values_list("pk", flat=True))
        return ElementType.objects.exclude(pk__in=pks)
