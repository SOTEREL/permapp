from django.contrib import admin

from ..mixins import LinkToProject
from ...forms.map import FeatureChangeForm, FeatureAddForm
from ...models.map import Feature, FeatureAttachment


class AttachmentInline(admin.TabularInline):
    model = FeatureAttachment


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin, LinkToProject):
    add_form = FeatureAddForm
    form = FeatureChangeForm
    list_display = ("name", "type", "link_to_project", "comments")
    list_filter = ("is_risky",)
    save_on_top = True
    search_fields = ("name", "comments", "project__name")
    inlines = [AttachmentInline]

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project", "type")
        return readonly_fields
