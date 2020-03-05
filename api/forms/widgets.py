import copy
import json

from django.forms import HiddenInput


class MapWidget(HiddenInput):
    template_name = "api/widgets/map.html"
    js_func = None
    js_args = None
    subfields = None

    class Media:
        css = {"all": ("api/css/leaflet.css",)}
        js = ("api/js/lib/leaflet.js", "api/js/map-tools.js", "api/js/widgets/map.js")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.js_args = copy.deepcopy(self.__class__.js_args or {})

    @property
    def is_hidden(self):
        return False

    def add_js_arg(self, key, value):
        if self.js_args is None:
            self.js_args = {}
        self.js_args[key] = value

    def get_context(self, name, value, attrs):
        widget_id = attrs["id"]
        attrs.update(
            field_template_name=super().template_name,
            map_id=widget_id + "_map",
            subfields=self.subfields or {},
            js_func=self.js_func or self.__class__.__name__,
            js_args=json.dumps(self.js_args),
        )
        return super().get_context(name, value, attrs)


class MapDrawingWidget(MapWidget):
    class Media:
        css = {"all": ("api/css/leaflet.draw.css",)}
        js = (
            "api/js/lib/leaflet.draw.js",
            "api/js/widgets/map-drawing.js",
        )
