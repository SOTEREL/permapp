from .shapes import GeoJSONShapeMapForm
from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Borders
from ...models.map.shapes import MultiPolygon


class BordersMapWidget(MapWidget):
    class Media:
        js = ("api/js/widgets/borders-map.js",)


class BordersForm(GeoJSONShapeMapForm, ProjectMapForm):
    map = AggregationField(
        ["is_from_parcels", "coordinates", "zoom", "map_projection"],
        widget=BordersMapWidget,
    )

    class Meta:
        model = Borders
        fields = ["project", "map"]

    @property
    def shape_class(self):
        return MultiPolygon
