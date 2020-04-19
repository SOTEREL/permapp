from rest_framework import serializers

from ...models.map import View, ViewFeature


class ViewFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ViewFeature
        fields = ("feature", "z_index", "min_zoom", "max_zoom")


class ViewSerializer(serializers.ModelSerializer):
    features = ViewFeatureSerializer(
        source="ordered_features", read_only=True, many=True
    )

    class Meta:
        model = View
        fields = "__all__"
