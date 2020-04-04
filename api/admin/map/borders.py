from django.contrib import admin

from ..mixins import LinkToProjectMixin
from ...forms.map import BordersForm
from ...models.map import Borders


@admin.register(Borders)
class BordersAdmin(admin.ModelAdmin, LinkToProjectMixin):
    list_display = ("__str__", "link_to_project")
    form = BordersForm
    save_on_top = True
    search_fields = ("project__name",)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields
