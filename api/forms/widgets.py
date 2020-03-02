import json

from django.forms import HiddenInput


class MapWidget(HiddenInput):
    template_name = "api/widgets/map.html"
    js_func = None
    js_args = None

    class Media:
        css = {"all": ("api/css/leaflet.css",)}
        js = ("api/js/lib/leaflet.js", "api/js/map-tools.js", "api/js/widgets/map.js")

    @property
    def is_hidden(self):
        return False

    def get_context(self, name, value, attrs):
        widget_id = attrs["id"]
        attrs.update(
            field_template_name=super().template_name,
            map_id=widget_id + "_map",
            js_func=self.js_func or self.__class__.__name__,
            js_args=self.js_args or {},
        )
        return super().get_context(name, value, attrs)
