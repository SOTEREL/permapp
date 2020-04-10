from rest_framework import serializers

from ...models.map import FeatureType
from .feature_style import FeatureStyleSerializer


class FeatureTypeSerializer(serializers.ModelSerializer):
    style = FeatureStyleSerializer()

    class Meta:
        model = FeatureType
        fields = "__all__"
