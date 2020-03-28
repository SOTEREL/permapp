from django.forms import ALL_FIELDS, ModelForm
from django_json_widget.widgets import JSONEditorWidget

from ...models.map import FeatureStyle


class FeatureStyleForm(ModelForm):
    class Meta:
        model = FeatureStyle
        fields = ALL_FIELDS
        widgets = {"style": JSONEditorWidget}
