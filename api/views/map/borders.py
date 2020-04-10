from rest_framework import viewsets

from ...models.map import Borders
from ...serializers.map import BordersSerializer


class BordersViewSet(viewsets.ModelViewSet):
    queryset = Borders.objects.all()
    serializer_class = BordersSerializer
    filterset_fields = ["project"]
