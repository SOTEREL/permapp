from rest_framework import serializers

from .models import MapElement, MapElementType, MapView, MapViewElement


class MapElementSerializer(serializers.ModelSerializer):
    shape = serializers.SerializerMethodField()

    class Meta:
        model = MapElement
        exclude = ["design", "polymorphic_ctype"]

    def get_shape(self, obj):
        return obj.json_shape


class MapElementTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapElementType
        exclude = ["polymorphic_ctype", "shape_ctype"]


class MapViewElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapViewElement
        exclude = ["view"]


class MapViewSerializer(serializers.ModelSerializer):
    elements = MapViewElementSerializer(many=True)

    class Meta:
        model = MapView
        exclude = ["design"]
