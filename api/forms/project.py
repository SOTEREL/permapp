import json

from django.forms import ModelForm, CharField, HiddenInput

from .aggregation import AggregationField, AggregationFormMixin
from ..models import Project


class MapSetupWidget(HiddenInput):
    template_name = "api/widgets/map_setup.html"

    class Media:
        css = {
            "all": ("https://unpkg.com/leaflet@1.6.0/dist/leaflet.css",),
        }
        js = (
            "https://unpkg.com/leaflet@1.6.0/dist/leaflet.js",
            "api/js/leaflet-tools.js",
        )

    @property
    def is_hidden(self):
        return False

    def get_context(self, name, value, attrs):
        widget_id = attrs["id"]
        attrs.update(
            field_template_name=super().template_name, map_id=widget_id + "_map",
        )
        return super().get_context(name, value, attrs)


class ProjectForm(ModelForm, AggregationFormMixin):
    map = AggregationField(["map_lat", "map_lng", "map_zoom"], widget=MapSetupWidget)

    class Meta:
        model = Project
        fields = ["name", "slug", "map", "map_lat", "map_lng", "map_zoom"]

    def __init__(self, *args, **kwargs):
        ModelForm.__init__(self, *args, **kwargs)
        AggregationFormMixin.__init__(self)
