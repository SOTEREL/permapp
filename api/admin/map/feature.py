from django.contrib import admin

from ..mixins import LinkToProject
from ...forms.map import make_feature_form
from ...models.map import Feature, FeatureAttachment


class AttachmentInline(admin.TabularInline):
    model = FeatureAttachment


class FeatureAbstractAdmin(admin.ModelAdmin, LinkToProject):
    list_display = ("name", "link_to_project", "comments", "permanence")
    list_filter = ("is_risky",)
    save_on_top = True
    search_fields = ("name", "comments", "project__name")
    inlines = [AttachmentInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields


def register_feature_admin(model, **kwargs):
    @admin.register(model)
    class FeatureAdmin(FeatureAbstractAdmin):
        form = make_feature_form(model, **kwargs)
