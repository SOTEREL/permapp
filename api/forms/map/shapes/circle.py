from ....models.map.shapes import Circle
from ...fields import AggregationField
from ...widgets import MapDrawingWidget
from .shape import ShapeForm


class CircleMapWidget(MapDrawingWidget):
    js_args = {"geom_type": "Circle"}

    class Media:
        js = ("api/js/widgets/feature-map.js", "api/js/widgets/circle-map.js")


class CircleForm(ShapeForm):
    map = AggregationField(
        ["coordinates", "map_projection", "radius"], widget=CircleMapWidget
    )

    class Meta:
        model = Circle
        fields = ["map"]
