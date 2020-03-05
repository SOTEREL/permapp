from ..fields import AggregationField
from ..project_map import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Point


class PointMapWidget(MapWidget):
    js_args = dict(project_field_id="id_project")

    class Media:
        css = {"all": ("api/css/leaflet.draw.css",)}
        js = ("api/js/lib/leaflet.draw.js", "api/js/widgets/point-map.js")


class PointForm(ProjectMapForm):
    map = AggregationField(["lat", "lng"], widget=PointMapWidget)

    class Meta:
        model = Point
        fields = ["project", "name", "map", "description"]
