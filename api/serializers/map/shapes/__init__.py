from rest_framework import serializers

from ....models.map.shapes import Shape, GeoJSONShape
from .shape import ShapeSerializer


def get_serializer_class(shape):
    if isinstance(shape, GeoJSONShape):
        return type(
            f"{shape.__class__.__name__}Serializer",
            (serializers.ModelSerializer,),
            {"Meta": type("Meta", (), {"model": shape.__class__, "fields": "__all__"})},
        )
    return ShapeSerializer
