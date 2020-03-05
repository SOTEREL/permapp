from ..fields import AggregationField
from ..forms import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Parcel


class ParcelMapWidget(MapWidget):
    class Media:
        js = ("api/js/lib/geoportal-access-lib.js", "api/js/widgets/parcel-map.js")


class ParcelForm(ProjectMapForm):
    map = AggregationField(
        ["insee", "section", "number", "geom"], widget=ParcelMapWidget
    )

    class Meta:
        model = Parcel
        fields = ["project", "map"]
