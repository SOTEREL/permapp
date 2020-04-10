from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Project
from ..models.map import Borders
from ..serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["get"])
    def borders(self, request, pk=None):
        borders = Borders.objects.get(project=pk)
        return Response(borders.shape.geojson)
