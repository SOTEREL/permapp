from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from shapely.geometry import mapping, shape, Polygon as PolygonShapely
from shapely.ops import unary_union

from .parcel import Parcel
from .shapes import Shape, MultiPolygon
from ..project import Project


class Borders(models.Model):
    project = models.OneToOneField(
        Project, related_name="borders", on_delete=models.CASCADE
    )
    is_from_parcels = models.BooleanField(default=True)
    shapes = GenericRelation(
        Shape,
        related_query_name="borders",
        content_type_field="content_type",
        object_id_field="object_id",
    )

    class Meta:
        verbose_name_plural = "borders"

    def __str__(self):
        return f"Borders of {self.project}"

    def coordinates_from_parcels(self):
        geoms = [
            shape(parcel.shape.geojson_geom) for parcel in self.project.parcels.all()
        ]
        union = unary_union(geoms)
        coordinates = mapping(union)["coordinates"]
        if isinstance(union, PolygonShapely):
            return [coordinates]
        return coordinates

    @property
    def coordinates(self):
        return self.shape.coordinates

    @property
    def shape(self):
        return self.shapes.first()


@receiver(post_save, sender=Project)
def create_from_project(sender, instance, created, **kwargs):
    if created:
        Borders.objects.create(project=instance)


@receiver(post_save, sender=Borders)
def create_shape(sender, instance, created, **kwargs):
    if created:
        MultiPolygon.objects.create(
            content_object=instance, coordinates=instance.coordinates_from_parcels()
        )


@receiver(post_save, sender=MultiPolygon)
def update_shape(sender, instance, created, **kwargs):
    if not isinstance(instance.content_object, Parcel):
        return
    project = instance.content_object.project
    try:
        borders = project.borders
    except Project.borders.RelatedObjectDoesNotExist:
        return
    if not borders.is_from_parcels:
        return
    shape = borders.shape
    shape.coordinates = borders.coordinates_from_parcels()
    shape.full_clean()
    shape.save()
