from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from ...models.map import Category, FeatureType


class FeatureTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureType
        fields = ("id", "slug", "name", "description")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")


class CategoryRecursiveSerializer(serializers.ModelSerializer):
    sub_categories = serializers.ListField(
        child=RecursiveField(), source="get_children"
    )
    feature_types = serializers.ListField(
        child=FeatureTypeSerializer(), source="feature_types.all"
    )

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "sub_categories", "feature_types")
