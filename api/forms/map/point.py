from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Point


class PointMapWidget(MapWidget):
    class Media:
        css = {"all": ("api/css/leaflet.draw.css",)}
        js = ("api/js/lib/leaflet.draw.js", "api/js/widgets/point-map.js")


class PointForm(ProjectMapForm):
    map = AggregationField(["lat", "lng"], widget=PointMapWidget)

    class Meta:
        model = Point
        fields = ["project", "name", "map", "description"]
