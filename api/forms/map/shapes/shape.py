from ...forms import AggregationForm
from ...widgets import MapWidget
from ....models.map import Feature
from ....models.map.shapes import Shape


class ShapeForm(AggregationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            ctype = self.instance.content_type
        except Shape.content_type.RelatedObjectDoesNotExist:
            ctype = None

        if ctype is not None:
            if issubclass(ctype.model_class(), Feature):
                style = self.instance.content_object.type.style
                if style is not None:
                    style = style.style

                project = self.instance.content_object.project
                map_center = dict(lng=project.map_lng, lat=project.map_lat)

                for field in self.fields.values():
                    if isinstance(field.widget, MapWidget):
                        field.widget.add_js_arg("mapCenter", map_center)
                        field.widget.add_js_arg("featureStyle", style)
