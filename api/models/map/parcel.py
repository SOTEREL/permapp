from django.core.validators import MinLengthValidator
from django.db import models

from jsonfield import JSONField

from ..project import Project


class Parcel(models.Model):
    # https://apicarto.ign.fr/api/doc/cadastre#/Parcelle/get_cadastre_parcelle
    project = models.ForeignKey(
        Project, related_name="parcels", on_delete=models.CASCADE
    )
    insee = models.CharField(max_length=5, validators=[MinLengthValidator(5)])
    section = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    number = models.CharField(max_length=4, validators=[MinLengthValidator(4)])
    geom = JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.number}-{self.section}-{self.insee}"
