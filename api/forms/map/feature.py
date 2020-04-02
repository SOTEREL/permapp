from django.conf import settings
from django.forms import IntegerField, ModelForm

from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from ..fields import AggregationField
from ..forms import ProjectMapForm
from ...models.map import Feature


class FeatureAddForm(ModelForm):
    class Meta:
        model = Feature
        fields = ("project", "type", "name")


class FeatureChangeForm(ModelForm):
    permanence = IntegerField(
        required=False, min_value=0, max_value=settings.FEATURE_PERMANENCE_MAX
    )

    class Meta:
        model = Feature
        fields = ("project", "type", "name", "is_risky", "permanence", "comments")
