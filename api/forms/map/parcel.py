from django.forms import ModelForm

from ..fields import AggregationField
from ..mixins import AggregationFormMixin, ProjectMapFormMixin
from ..widgets import MapWidget
from ...models.map import Parcel


class ParcelMapWidget(MapWidget):
    js_args = dict(project_field_id="id_project")

    class Media:
        js = (
            "https://ignf.github.io/geoportal-access-lib/latest/dist/GpServices.js",
            "api/js/widgets/parcel-map.js",
        )


class ParcelForm(ModelForm, AggregationFormMixin, ProjectMapFormMixin):
    map = AggregationField(
        ["insee", "section", "number", "geom"], widget=ParcelMapWidget
    )

    class Meta:
        model = Parcel
        fields = ["project", "map", "insee", "section", "number", "geom"]

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        AggregationFormMixin.__init__(self)
        ProjectMapFormMixin.__init__(self)
