from rest_framework.response import Response
from rest_framework import viewsets

from ...models.map import Category
from ...serializers.map import CategoryRecursiveSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryRecursiveSerializer

    def list(self, request):
        categories = [
            CategoryRecursiveSerializer(root).data
            for root in Category.tree.root_nodes()
        ]
        return Response(categories)
