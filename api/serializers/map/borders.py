from rest_framework import serializers

from ...models.map import Borders


class BordersSerializer(serializers.ModelSerializer):
    geojson_geom = serializers.JSONField(source="shape.geojson_geom")
    map_projection = serializers.CharField(source="shape.map_projection")

    class Meta:
        model = Borders
        fields = "__all__"
