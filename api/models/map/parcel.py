from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .shapes import Shape, MultiPolygon
from ..project import Project
from ...geoportal import parcel_coordinates, ParcelCoordinatesNotFoundError


class Parcel(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    # https://apicarto.ign.fr/api/doc/cadastre#/Parcelle/get_cadastre_parcelle
    insee = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    section = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    number = models.CharField(max_length=4, validators=[MinLengthValidator(4)])
    shapes = GenericRelation(
        Shape,
        related_query_name="parcel",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    _coordinates = None  # Cache api response

    class Meta:
        unique_together = ("project", "insee", "section", "number")

    def __str__(self):
        return f"{self.number}-{self.section}-{self.insee}"

    def validate_parcel_coordinates(self, insee, section, number):
        try:
            self._coordinates = parcel_coordinates(insee, section, number)
        except ParcelCoordinatesNotFoundError as e:
            raise ValidationError(f"Cannot find the coordinates of the parcel {self}")

    def clean(self):
        super().clean()
        self.validate_parcel_coordinates(self.insee, self.section, self.number)

    @property
    def shape(self):
        return self.shapes.first()


@receiver(post_save, sender=Parcel)
def create_shape(sender, instance, created, **kwargs):
    if created:
        MultiPolygon.objects.create(
            content_object=instance, coordinates=instance._coordinates
        )
    else:
        shape = instance.shape
        shape.coordinates = instance._coordinates
        shape.save()
