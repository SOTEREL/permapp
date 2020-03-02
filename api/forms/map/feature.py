from django.forms import ModelForm

from ..fields import AggregationField
from ..mixins import AggregationFormMixin, ProjectMapFormMixin
from ..widgets import MapWidget
from ...models.map import Feature


class FeatureMapWidget(MapWidget):
    js_args = dict(project_field_id="id_project")

    class Media:
        css = {"all": ("api/css/leaflet.draw.css",)}
        js = ("api/js/lib/leaflet.draw.js", "api/js/widgets/feature-map.js")


class FeatureForm(ModelForm, AggregationFormMixin, ProjectMapFormMixin):
    map = AggregationField(["geom"], widget=FeatureMapWidget)

    class Meta:
        model = Feature
        fields = ["project", "name", "description", "geom"]

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        AggregationFormMixin.__init__(self)
        ProjectMapFormMixin.__init__(self)
