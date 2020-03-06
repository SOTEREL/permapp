from django.core.validators import MinLengthValidator
from django.db import models

from .polygon import MultiPolygonBase


class Parcel(MultiPolygonBase):
    # https://apicarto.ign.fr/api/doc/cadastre#/Parcelle/get_cadastre_parcelle
    insee = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    section = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    number = models.CharField(max_length=4, validators=[MinLengthValidator(4)])

    class Meta:
        pass
        # TODO: project field doesn't exist in this table
        # unique_together = ("project", "insee", "section", "number")

    def __str__(self):
        return f"{self.number}-{self.section}-{self.insee}"
