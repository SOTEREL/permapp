from .fields import AggregationField
from .aggregation import AggregationForm
from .widgets import MapWidget
from ..models import Project


class ProjectMapWidget(MapWidget):
    class Media:
        js = ("api/js/widgets/project-map.js",)


class ProjectForm(AggregationForm):
    map = AggregationField(["map_lat", "map_lng", "map_zoom"], widget=ProjectMapWidget)

    class Meta:
        model = Project
        fields = ["name", "slug", "map"]
