from django.contrib.contenttypes.models import ContentType
from django.db import models

from .element_type import ElementType
from .validators import validate_shape_ctype


class Theme(models.Model):
    name = models.CharField(max_length=50, unique=True)
    element_types = models.ManyToManyField(ElementType, through="ThemedElementType",)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def missing_element_types(self):
        pks = list(self.element_types.values_list("pk", flat=True))
        return ElementType.objects.exclude(pk__in=pks)


class ThemedElementType(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    element_type = models.ForeignKey(ElementType, on_delete=models.CASCADE)
    shape_ctype = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        related_name="+",
        validators=[validate_shape_ctype],
    )

    # TODO: define zoom range so that we can have different styles depending on
    # the zoom level

    class Meta:
        ordering = ["theme", "element_type"]
        unique_together = ("theme", "element_type")

    @classmethod
    def list_usable_shape_ctypes(cls, as_queryset=False):
        from .shapes import usable_shape_models

        ctypes = ContentType.objects.get_for_models(*usable_shape_models).values()
        if as_queryset:
            return ContentType.objects.filter(pk__in=[ctype.pk for ctype in ctypes])
        return ctypes

    def __str__(self):
        return f"{self.element_type} (theme: {self.theme})"

    @property
    def shape_cls(self):
        return self.shape_ctype.model_class()
