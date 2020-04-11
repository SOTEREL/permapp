from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ...models.map import Feature
from ...serializers.map import FeatureSerializer, FeatureDrawingSerializer


class FeatureViewSet(viewsets.ModelViewSet):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filterset_fields = ["project"]

    @action(detail=True, methods=["get"])
    def drawing(self, request, pk=None):
        feature = Feature.objects.get(pk=pk)
        serializer = FeatureDrawingSerializer(feature)
        return Response(serializer.data)
