from django.views.generic import DetailView, ListView

from .models import Design, MapElement, MapElementType, MapView
from .serializers import (
    MapElementSerializer,
    MapElementTypeSerializer,
    MapViewSerializer,
)


class DesignListView(ListView):
    model = Design
    template_name = "designs/list.html"
    context_object_name = "designs"


class DesignMapView(DetailView):
    model = Design
    template_name = "designs/map.html"
    context_object_name = "design"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        map_elements = MapElement.objects.filter(design=self.object)
        map_element_type_pks = set(
            map_elements.values_list("element_type__pk", flat=True)
        )
        context["js_data"] = {
            "mapElements": {
                e["id"]: e for e in MapElementSerializer(map_elements, many=True).data
            },
            "mapElementTypes": {
                t["id"]: t
                for t in MapElementTypeSerializer(
                    MapElementType.objects.filter(pk__in=map_element_type_pks),
                    many=True,
                ).data
            },
            "mapViews": MapViewSerializer(
                MapView.objects.filter(design=self.object), many=True
            ).data,
        }
        return context
