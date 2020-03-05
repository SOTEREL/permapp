from ..fields import AggregationField
from ..project_map import ProjectMapForm
from ..widgets import MapWidget
from ...models.map import Parcel


class ParcelMapWidget(MapWidget):
    js_args = dict(project_field_id="id_project")

    class Media:
        js = ("api/js/lib/geoportal-access-lib.js", "api/js/widgets/parcel-map.js")


class ParcelForm(ProjectMapForm):
    map = AggregationField(
        ["insee", "section", "number", "geom"], widget=ParcelMapWidget
    )

    class Meta:
        model = Parcel
        fields = ["project", "map"]
