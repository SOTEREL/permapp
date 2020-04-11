from rest_framework import serializers

from ....models.map.shapes import Shape, GeoJSONShape
from .shape import ShapeSerializer, ShapeDrawingSerializer


def get_serializer_class(shape):
    if isinstance(shape, GeoJSONShape):
        Meta = type("Meta", (), {"model": shape.__class__, "fields": "__all__"})
        return type(
            f"{shape.__class__.__name__}Serializer",
            (serializers.ModelSerializer,),
            {"Meta": Meta},
        )
    return ShapeSerializer


def get_drawing_serializer_class(shape):
    if isinstance(shape, GeoJSONShape):
        Meta = type(
            "Meta",
            (),
            {
                "model": shape.__class__,
                "fields": ("id", "map_projection", "zoom", "geojson_geom"),
            },
        )
        return type(
            f"{shape.__class__.__name__}DrawingSerializer",
            (serializers.ModelSerializer,),
            {"Meta": Meta},
        )
    return ShapeDrawingSerializer
