from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin

from ..models import MapView, MapViewElement


class DesignFilter(AutocompleteFilter):
    title = "design"
    field_name = "design"


class MapViewElementInline(admin.TabularInline):
    model = MapViewElement
    autocomplete_fields = ("map_element",)


@admin.register(MapView)
class MapViewAdmin(admin.ModelAdmin):
    inlines = [MapViewElementInline]
    list_display = ("name", "design")
    list_filter = (DesignFilter,)
    search_fields = ("name", "design__name")
    autocomplete_fields = ("design",)
