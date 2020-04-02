from django.contrib import admin

from ...forms.map import FeatureStyleForm
from ...models.map import FeatureStyle


@admin.register(FeatureStyle)
class FeatureStyleAdmin(admin.ModelAdmin):
    list_display = ("name", "shape_ctype")
    form = FeatureStyleForm
    save_on_top = True
