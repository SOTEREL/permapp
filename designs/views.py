from django.views.generic import DetailView, ListView

from .models import Design


class DesignListView(ListView):
    model = Design
    template_name = "designs/list.html"
    context_object_name = "designs"


class DesignMapView(DetailView):
    model = Design
    template_name = "designs/map.html"
    context_object_name = "design"
