from rest_framework import viewsets

from ...models.map import Parcel
from ...serializers.map import ParcelSerializer


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filterset_fields = ["project", "section", "insee"]

    def get_queryset(self):
        print(self.request.query_params)
        return super().get_queryset()
