from django.forms import ModelForm

from ..aggregation import AggregationField, AggregationFormMixin
from ..widgets import MapWidget
from ...models.map import Parcel


class ParcelMapWidget(MapWidget):
    class Media:
        js = (
            "https://ignf.github.io/geoportal-access-lib/latest/dist/GpServices.js",
            "api/js/widgets/parcel-map.js",
        )


class ParcelForm(ModelForm):
    map = AggregationField(
        ["insee", "section", "number", "geom"], widget=ParcelMapWidget
    )

    class Meta:
        model = Parcel
        fields = ["project", "map", "insee", "section", "number", "geom"]

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        AggregationFormMixin.__init__(self)
