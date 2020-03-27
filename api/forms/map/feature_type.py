from django.forms import ALL_FIELDS, ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ...models.map import FeatureType


class FeatureTypeForm(ModelForm):
    class Meta:
        model = FeatureType
        fields = ALL_FIELDS
        widgets = {"extra_props_schema": JSONEditorWidget}
