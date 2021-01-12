from django.conf import settings
from django.db import models
from polymorphic.managers import PolymorphicManager
from polymorphic.models import PolymorphicModel
from tagging.registry import register as tagging_register

from .design import Design
from .element_type import ElementType


class ElementManager(PolymorphicManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                is_observation=models.ExpressionWrapper(
                    models.Q(observation_date__isnull=False),
                    output_field=models.BooleanField(),
                )
            )
        )


class Element(PolymorphicModel):
    design = models.ForeignKey(Design, on_delete=models.CASCADE)
    element_type = models.ForeignKey(ElementType, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(default="", blank=True)
    needs = models.TextField(default="", blank=True)
    contributions = models.TextField(default="", blank=True)
    observation_date = models.DateField(null=True, blank=True)
    permanence = models.PositiveSmallIntegerField(
        null=True, blank=True, choices=settings.PERMANENCE_CHOICES
    )
    is_risky = models.BooleanField(default=False)

    objects = ElementManager()

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def all_tags(self):
        return self.element_type.tags.all() | self.tags.all()


tagging_register(Element)


class MapElement(Element):
    @property
    def style(self):
        map_theme = self.design.map_theme
        return self.element_type.styles.filter(map_theme=map_theme).first()

    @property
    def json_style(self):
        style = self.style
        if style is None:
            return {}
        return style.to_json()
