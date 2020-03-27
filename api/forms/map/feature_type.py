from django.forms import ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ...models.map import FeatureType


class FeatureTypeForm(ModelForm):
    class Meta:
        model = FeatureType
        fields = ["name", "slug", "category", "extra_props_schema"]
        widgets = {"extra_props_schema": JSONEditorWidget}
