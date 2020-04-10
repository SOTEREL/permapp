from rest_framework.response import Response
from rest_framework import viewsets

from ...models.map import FeatureType
from ...serializers.map import FeatureTypeSerializer


class FeatureTypeViewSet(viewsets.ModelViewSet):
    queryset = FeatureType.objects.all()
    serializer_class = FeatureTypeSerializer
