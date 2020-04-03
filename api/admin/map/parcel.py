from django.contrib import admin

from ..mixins import LinkToProjectMixin
from ...forms.map import ParcelForm
from ...models.map import Parcel


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin, LinkToProjectMixin):
    list_display = ("number", "link_to_project", "insee", "section")
    form = ParcelForm
    save_on_top = True
    search_fields = ("project__name",)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields
