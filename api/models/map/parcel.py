from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .polygon import MultiPolygonBase


class Parcel(MultiPolygonBase):
    # https://apicarto.ign.fr/api/doc/cadastre#/Parcelle/get_cadastre_parcelle
    insee = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    section = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    number = models.CharField(max_length=4, validators=[MinLengthValidator(4)])

    def __str__(self):
        return f"{self.number}-{self.section}-{self.insee}"

    def validate_unique(self, *args, **kwargs):
        super().validate_unique(*args, **kwargs)

        # We cannot check uniqueness wtih Meta.unique_together due to multi-table inheritance
        qs = Parcel.objects.filter(project=self.project).exclude(pk=self.pk)
        if qs.filter(
            insee=self.insee, section=self.section, number=self.number
        ).exists():
            raise ValidationError(
                _(f"This parcel is already registered for this project")
            )
