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
        fields = (
            "project",
            "type",
            "name",
            "is_risky",
            "permanence",
            "comments",
            "extra_props",
            "style",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        feature_type = self.instance.type

        self.fields["style"].queryset = self.fields["style"].queryset.filter(
            feature_type=feature_type
        )

        extra_props_schema = feature_type.extra_props_schema
        if extra_props_schema is None:
            self.fields["extra_props"].widget = self.fields[
                "extra_props"
            ].hidden_widget()
        else:
            self.fields["extra_props"].widget = JSONSchemaWidget(extra_props_schema)
