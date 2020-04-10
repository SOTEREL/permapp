from rest_framework import serializers

from ....models.map.shapes import Shape


class ShapeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shape
        fields = "__all__"
