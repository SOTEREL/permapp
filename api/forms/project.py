from django.forms import ModelForm

from .aggregation import AggregationField, AggregationFormMixin
from .widgets import MapWidget
from ..models import Project


class ProjectMapWidget(MapWidget):
    js_func = "ProjectMapWidget"

    class Media:
        js = ("api/js/widgets/project-map.js",)


class ProjectForm(ModelForm, AggregationFormMixin):
    map = AggregationField(["map_lat", "map_lng", "map_zoom"], widget=ProjectMapWidget)

    class Meta:
        model = Project
        fields = ["name", "slug", "map", "map_lat", "map_lng", "map_zoom"]

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        AggregationFormMixin.__init__(self)
