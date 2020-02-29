from django.forms import HiddenInput


class MapWidget(HiddenInput):
    template_name = "api/widgets/map.html"
    js_func = None

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
            field_template_name=super().template_name,
            map_id=widget_id + "_map",
            js_func=self.js_func or self.__class__.__name__,
        )
        return super().get_context(name, value, attrs)
