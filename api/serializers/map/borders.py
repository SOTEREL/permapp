from rest_framework import serializers

from ...models.map import Borders


class BordersSerializer(serializers.ModelSerializer):
    geojson = serializers.JSONField(source="shape.geojson")

    class Meta:
        model = Borders
        fields = "__all__"
