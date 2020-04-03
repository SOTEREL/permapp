from django.conf import settings
from django.forms import IntegerField, ModelForm, modelform_factory

from jsonschemaform.admin.widgets.jsonschema_widget import JSONSchemaWidget

from ..fields import AggregationField, FeatureTypeField
from ..forms import ProjectMapForm
from ...models.map import Feature, FeatureType


def make_feature_add_form(model, fields=None, **kwargs):
    if fields is None:
        fields = ("project", "type", "name")

    form = type("BaseFeatureAddForm", (ModelForm,), {})
    if "type" in fields:
        setattr(form, "type", FeatureTypeField(model))

    return modelform_factory(model, form=form, fields=fields, **kwargs)


class FeatureAddForm(ModelForm):
    class Meta:
        model = Feature
        fields = ("project", "type", "name")


class FeatureAddTypeForm(ModelForm):
    class Meta:
        model = Feature
        fields = ("type",)


def make_feature_change_form(model, fields=None, extra_fields=None, **kwargs):
    if fields is None:
        fields = ("project", "type", "name", "is_risky", "permanence", "comments")
    if extra_fields is not None:
        fields = (*fields, *extra_fields)

    form = type("BaseFeatureChangeForm", (ModelForm,), {})
    if "permanence" in fields:
        setattr(
            form,
            "permanence",
            IntegerField(
                required=False, min_value=0, max_value=settings.FEATURE_PERMANENCE_MAX
            ),
        )
    return modelform_factory(model, form=form, fields=fields, **kwargs)
