from django.contrib import admin

from .feature import BaseFeatureAdmin
from ...forms.map import make_feature_add_form, make_feature_change_form
from ...models.map import Building


@admin.register(Building)
class FeatureAdmin(BaseFeatureAdmin):
    add_form = make_feature_add_form(Building)
    form = make_feature_change_form(Building, extra_fields=("roof_surface",))
