from .shapes import GeoJSONShapeMapForm
from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Parcel
from ...models.map.shapes import MultiPolygon


class ParcelMapWidget(MapWidget):
    class Media:
        js = ("api/js/lib/geoportal-access-lib.js", "api/js/widgets/parcel-map.js")


class ParcelForm(GeoJSONShapeMapForm, ProjectMapForm):
    map = AggregationField(
        ["insee", "section", "number", "coordinates", "zoom", "map_projection"],
        widget=ParcelMapWidget,
    )

    class Meta:
        model = Parcel
        fields = ["project", "map"]

    @property
    def shape_class(self):
        return MultiPolygon
