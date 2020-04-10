from rest_framework import viewsets

from ..models import Project
from ..models.map import Borders
from ..serializers import ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
