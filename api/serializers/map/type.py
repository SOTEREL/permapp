from rest_framework import serializers

from .category import CategorySerializer
from ...models.map import Type


class TypeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Type
        fields = ("slug", "name", "category")
