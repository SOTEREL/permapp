from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ...models.map import View
from ...serializers.map import ViewSerializer


class ViewViewSet(viewsets.ModelViewSet):
    queryset = View.objects.all()
    serializer_class = ViewSerializer
    filterset_fields = ["project"]
