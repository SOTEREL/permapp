from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ...models.map import Feature
from ...serializers.map import FeatureSerializer, FeatureDetailSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    filterset_fields = ["project"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return FeatureDetailSerializer
        return FeatureSerializer
