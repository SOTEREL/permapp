from ...forms import AggregationForm
from ...widgets import MapWidget


class ShapeForm(AggregationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None and self.instance.feature_id is not None:
            style = self.instance.feature.type.style
            if style is not None:
                style = style.style

            project = self.instance.feature.project
            map_center = dict(lng=project.map_lng, lat=project.map_lat)

            for field in self.fields.values():
                if isinstance(field.widget, MapWidget):
                    field.widget.add_js_arg("mapCenter", map_center)
                    field.widget.add_js_arg("featureStyle", style)
