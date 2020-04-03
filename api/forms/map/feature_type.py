from django.forms import ALL_FIELDS, ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ..fields import ShapeCtypeField
from ...models.map import FeatureType


class FeatureTypeForm(ModelForm):
    shape_ctype = ShapeCtypeField()

    class Meta:
        model = FeatureType
        fields = ALL_FIELDS

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            field = self.fields["style"]
            shape_ctype = self.instance.shape_ctype
        except (KeyError, FeatureType.shape_ctype.RelatedObjectDoesNotExist):
            pass
        else:
            field.queryset = field.queryset.filter(shape_ctype=shape_ctype)
