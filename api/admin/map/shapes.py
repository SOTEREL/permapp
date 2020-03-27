from django.contrib import admin

from ...forms.map import shapes as shape_forms
from ...models.map import shapes as shape_models


for name in ["Circle", "Line", "MultiPolygon", "Point", "Polygon"]:
    model = getattr(shape_models, name)

    @admin.register(model)
    class ShapeAdmin(admin.ModelAdmin):
        form = getattr(shape_forms, f"{name}Form", shape_forms.make_geojson_form(model))
