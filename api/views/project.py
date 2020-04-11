from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from ..models import Project
from ..models.map import Borders
from ..serializers import ProjectSerializer
from ..serializers.map import BordersSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["get"])
    def borders(self, request, pk=None):
        borders = Borders.objects.get(project=pk)
        serializer = BordersSerializer(borders)
        return Response(serializer.data)
