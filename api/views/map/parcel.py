from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from shapely.geometry import mapping, shape
from shapely.ops import unary_union

from ...models.map import Parcel
from ...serializers.map import ParcelSerializer


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer
    filterset_fields = ["project", "section", "insee"]

    @action(detail=False)
    def union(self, request):
        # TODO:
        # https://gis.stackexchange.com/questions/166675/what-units-are-used-by-geopandas-shapely-area-and-distance-functions
        qs = (
            self.filter_queryset(self.get_queryset())
            .filter(geom__isnull=False)
            .values_list("geom", flat=True)
        )
        shapes = list(map(shape, qs))
        union = unary_union(shapes)
        try:
            n_polygons = len(union)
        except TypeError:
            n_polygons = 1

        return Response(
            dict(
                area=union.area,
                bounds=union.bounds,
                perimeter=union.length,
                n_polygons=n_polygons,
                geom=mapping(union),
            )
        )
