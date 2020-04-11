from rest_framework import serializers

from ...models.map import FeatureStyle


class FeatureStyleSerializer(serializers.ModelSerializer):
    style = serializers.JSONField()

    class Meta:
        model = FeatureStyle
        fields = "__all__"
