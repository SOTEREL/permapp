from rest_framework import serializers

from ...models.map import Feature
from .feature_type import FeatureTypeSerializer
from .shapes import ShapeSerializer, get_serializer_class


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class FeatureDetailSerializer(serializers.ModelSerializer):
    type = FeatureTypeSerializer()
    shape = ShapeSerializer(read_only=True)

    class Meta:
        model = Feature
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["shape"] = get_serializer_class(self.instance.shape)(
                read_only=True
            )
