from django.forms import ALL_FIELDS, ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ..fields import ShapeCtypeField
from ...models.map import FeatureStyle


class FeatureStyleForm(ModelForm):
    shape_ctype = ShapeCtypeField()

    class Meta:
        model = FeatureStyle
        fields = ALL_FIELDS
        widgets = {"style": JSONEditorWidget}
