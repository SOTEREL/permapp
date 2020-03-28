from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline

from ..mixins import LinkToProject
from ...forms.map import FeatureChangeForm, FeatureAddForm, shapes as shape_forms
from ...models.map import Feature, FeatureAttachment


class AttachmentInline(admin.TabularInline):
    model = FeatureAttachment


@admin.register(Feature)
class FeatureAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin, LinkToProject):
    form = FeatureChangeForm
    list_display = ("name", "type", "link_to_project", "comments")
    list_filter = ("is_risky",)
    save_on_top = True
    search_fields = ("name", "comments", "project__name")

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = FeatureAddForm
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project", "type")
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        ShapeInline = type(
            "ShapeInline",
            (admin.StackedInline,),
            {
                "model": obj.shape_model,
                "form": getattr(
                    shape_forms,
                    f"{obj.shape_model.__name__}Form",
                    shape_forms.make_geojson_form(obj.shape_model),
                ),
                "readonly_fields": ["shape_ptr"],
                "can_delete": False,
                "extra": 0,
            },
        )

        return [
            ShapeInline(self.model, self.admin_site),
            AttachmentInline(self.model, self.admin_site),
        ]
