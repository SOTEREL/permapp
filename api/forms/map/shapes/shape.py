from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.forms import modelform_factory, IntegerField, CharField

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


class ShapeMapForm(AggregationForm):
    map_projection = CharField()
    zoom = IntegerField(min_value=0, initial=settings.SATELLITE_LAYER_MAX_ZOOM)
    shape_fields = ["map_projection", "zoom"]

    def __init__(self, *args, **kwargs):
        # Must be done before init so that it's included to the map field initial
        self._set_shape_initials(kwargs.get("instance"))
        super().__init__(*args, **kwargs)

    def _set_shape_initials(self, instance):
        if instance is None:
            return
        for field in self.shape_fields:
            self.base_fields[field].initial = getattr(
                instance.shape, field, self.base_fields[field].initial
            )

    @property
    def shape_class(self):
        raise NotImplementedError(
            f"{self.__class__._name__}.shape_class must be defined"
        )

    @property
    def shape_form_class(self):
        return modelform_factory(self.shape_class)

    def full_clean(self):
        super().full_clean()
        shape_form = self.shape_form_class(data=self.data)
        shape_form.full_clean()
