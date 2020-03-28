from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from ..mixins import LinkToProject
from ...forms.map import FeatureChangeForm, FeatureAddForm, shapes as shape_forms
from ...models.map import Feature, FeatureAttachment
from ...models.map import shapes as shape_models


class AttachmentInline(admin.TabularInline):
    model = FeatureAttachment


class ShapeInline(StackedPolymorphicInline):
    model = shape_models.Shape
    can_delete = False
    extra = 0
    child_inlines = [
        type(
            f"{model_name}Inline",
            (StackedPolymorphicInline.Child,),
            {
                "model": getattr(shape_models, model_name),
                "form": getattr(
                    shape_forms,
                    f"{model_name}Form",
                    shape_forms.make_geojson_form(getattr(shape_models, model_name)),
                ),
            },
        )
        for model_name in ["Circle", "Line", "MultiPolygon", "Point", "Polygon"]
    ]


@admin.register(Feature)
class FeatureAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin, LinkToProject):
    add_form = FeatureAddForm
    form = FeatureChangeForm
    list_display = ("name", "type", "link_to_project", "comments")
    list_filter = ("is_risky",)
    save_on_top = True
    search_fields = ("name", "comments", "project__name")
    inlines = [ShapeInline, AttachmentInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project", "type")
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []
        return [inline(self.model, self.admin_site) for inline in self.inlines]

    """
    def link_to_shape(self, obj):
        shape_model_name = obj.type.shape_model
        reverse_name = shape_model_name.lower()
        link = reverse(f"admin:api_{reverse_name}_change", args=[obj.shape.pk])
        return format_html('<a href="{}">{}</a>', link, shape_model_name)

    link_to_shape.short_description = "shape"
    """
