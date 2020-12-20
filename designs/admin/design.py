from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from leaflet.admin import LeafletGeoAdminMixin

from ..forms import DesignAdminForm
from ..models import Design


class CreatorFilter(AutocompleteFilter):
    title = "creator"
    field_name = "creator"


@admin.register(Design)
class DesignAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    form = DesignAdminForm
    list_display = ("name", "creator")
    list_filter = (CreatorFilter,)
    search_fields = ("name",)
    autocomplete_fields = ("creator",)
    prepopulated_fields = {"slug": ("name",)}

    class Media:
        js = ("designs/admin/design.js",)

    def get_changeform_initial_data(self, request):
        return {"creator": request.user}

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if request.user.is_superuser:
            return fields
        return [*fields, "creator"]
