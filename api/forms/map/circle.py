from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget
from ...models.map import Circle


class CircleMapWidget(MapDrawingWidget):
    class Media:
        js = ("api/js/widgets/feature-map.js", "api/js/widgets/circle-map.js")


class CircleForm(ProjectMapForm):
    map = AggregationField(
        ["coordinates", "radius", "projection"], widget=CircleMapWidget
    )

    class Meta:
        model = Circle
        fields = ["project", "name", "map", "description", "style"]
