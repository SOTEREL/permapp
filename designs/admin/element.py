import html
import json

from admin_auto_filters.filters import AutocompleteFilter
from django.conf import settings
from django.contrib import admin
from django.forms import modelform_factory
from django.utils.html import format_html
from leaflet.admin import LeafletGeoAdminMixin
from permapp.admin import get_instance_href

from ..forms import MapShapeAdminForm
from ..models import ElementType, MapElement, MapElementType


class DesignFilter(AutocompleteFilter):
    title = "design"
    field_name = "design"


class ElementTypeFilter(AutocompleteFilter):
    title = "element type"
    field_name = "element_type"


class ElementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "design_html",
        "element_type_html",
        "description_html",
        "needs_html",
        "contributions_html",
    )
    list_filter = (DesignFilter, ElementTypeFilter, "permanence", "is_risky")
    search_fields = ("name", "design__name", "element_type__name")
    autocomplete_fields = ("design", "element_type")

    def design_html(self, obj):
        return format_html(get_instance_href(obj.design))

    design_html.short_description = "design"
    design_html.admin_order_field = "design"

    def element_type_html(self, obj):
        return format_html(get_instance_href(obj.element_type))

    element_type_html.short_description = "type"
    element_type_html.admin_order_field = "element_type"

    def _format_text_field(self, obj, field):
        escaped = html.escape(getattr(obj, field))
        return format_html(escaped.replace("\n", "<br />"))

    def description_html(self, obj):
        return self._format_text_field(obj, "description")

    description_html.short_description = "description"

    def needs_html(self, obj):
        return self._format_text_field(obj, "needs")

    needs_html.short_description = "needs"

    def contributions_html(self, obj):
        return self._format_text_field(obj, "contributions")

    contributions_html.short_description = "contributions"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "element_type":
            kwargs["queryset"] = ElementType.objects.not_instance_of(MapElementType)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MapElement)
class MapElementAdmin(ElementAdmin):
    readonly_fields = ("json_str_style",)

    class Media:
        js = ("designs/admin/map_element.js",)

    def json_str_style(self, obj):
        return json.dumps(obj.json_style)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "element_type":
            kwargs["queryset"] = ElementType.objects.instance_of(MapElementType)
        # Do not call super() as it would override the queryset through
        # ElementAdmin.formfield_for_foreignkey()
        return admin.ModelAdmin.formfield_for_foreignkey(
            self, db_field, request, **kwargs
        )

    def get_inlines(self, request, obj):
        if obj is None:
            return []
        inlines = super().get_inlines(request, obj)
        shape_inline = type(
            "ShapeInline",
            (LeafletGeoAdminMixin, admin.StackedInline),
            {
                "model": obj.element_type.shape_cls,
                "form": modelform_factory(
                    obj.element_type.shape_cls, form=MapShapeAdminForm
                ),
                "readonly_fields": ("map_projection",),
                "settings_overrides": {
                    "DEFAULT_CENTER": tuple(
                        reversed(obj.design.map_center["coordinates"])
                    ),
                    "DEFAULT_ZOOM": settings.DEFAULT_SHAPE_EDIT_ZOOM,
                },
            },
        )
        return [*inlines, shape_inline]
