from django.contrib import admin

from ..mixins import LinkToProject


class FeatureAbstractAdmin(admin.ModelAdmin, LinkToProject):
    list_display = ("name", "link_to_project", "description")
    save_on_top = True
    search_fields = ("name", "description", "project__name")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields
