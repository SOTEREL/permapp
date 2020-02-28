from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ...models.map import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class CategoryRecursiveSerializer(serializers.ModelSerializer):
    children = serializers.ListField(child=RecursiveField(), source="get_children")

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "children")
