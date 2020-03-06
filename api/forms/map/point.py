from django_json_widget.widgets import JSONEditorWidget

from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapDrawingWidget
from ...models.map import Point


class PointMapWidget(MapDrawingWidget):
    class Media:
        js = ("api/js/widgets/point-map.js",)


class PointForm(ProjectMapForm):
    map = AggregationField(["coordinates", "projection"], widget=PointMapWidget)

    class Meta:
        model = Point
        fields = ["project", "name", "map", "description", "style"]
        widgets = {"style": JSONEditorWidget}
