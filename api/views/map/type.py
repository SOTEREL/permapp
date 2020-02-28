from itertools import chain

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import viewsets

from ...models import Project
from ...models.map import Type
from ...serializers.map import TypeSerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def get_queryset(self):
        try:
            project = self.request.query_params["project"]
        except KeyError:
            return self.queryset

        project = get_object_or_404(Project, pk=project)
        return chain(self.queryset, project.custom_map_types.all())

    """
    def list(self, request):
        serializer = TypeSerializer(self.get_queryset())
        cat = next(qs).category
        categories = [
            CategoryRecursiveSerializer(root).data
            for root in Category.tree.root_nodes()
        ]
        return Response(categories)
        try:
            project = request.query_params["project"]
        except KeyError:
            return super().list(request)

        queryset = chain(Type.objects.all(), project.custom_map_types.all())
        serializer = TypeSerializer(queryset, many=True)
        return Response(serializer.data)
    """
