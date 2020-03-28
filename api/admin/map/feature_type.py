from django.contrib import admin

from ...forms.map import FeatureTypeForm
from ...models.map import FeatureType


@admin.register(FeatureType)
class FeatureTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "shape_model")
    form = FeatureTypeForm
    prepopulated_fields = {"slug": ("name",)}
    save_on_top = True
