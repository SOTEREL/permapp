from rest_framework import serializers

from ...models.map import Feature
from .feature_style import FeatureStyleSerializer
from .feature_type import FeatureTypeSerializer
from .shapes import ShapeDrawingSerializer, get_drawing_serializer_class


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class FeatureDrawingSerializer(serializers.ModelSerializer):
    style = FeatureStyleSerializer(source="type.style")
    shape = ShapeDrawingSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = ("shape", "style")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["shape"] = get_drawing_serializer_class(self.instance.shape)(
                read_only=True
            )
