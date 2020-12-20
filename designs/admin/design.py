from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from leaflet.admin import LeafletGeoAdminMixin

from ..models import Design


class CreatorFilter(AutocompleteFilter):
    title = "creator"
    field_name = "creator"


@admin.register(Design)
class DesignAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ("name", "creator")
    list_filter = (CreatorFilter,)
    search_fields = ("name",)
    autocomplete_fields = ("creator",)
    prepopulated_fields = {"slug": ("name",)}

    def get_changeform_initial_data(self, request):
        return {"creator": request.user}
