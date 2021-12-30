import json

from admin_auto_filters.filters import AutocompleteFilter
from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import modelform_factory
from leaflet.admin import LeafletGeoAdminMixin
from tagging.models import TaggedItem

from ..forms import MapShapeAdminForm
from ..models import ElementAttachment, ElementType, MapElement, MapElementType


class DesignFilter(AutocompleteFilter):
    title = "design"
    field_name = "design"


class ElementTypeFilter(AutocompleteFilter):
    title = "element type"
    field_name = "element_type"


class ElementAttachmentInline(admin.TabularInline):
    model = ElementAttachment


class ElementTagsInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ("tag",)


class ElementAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "design",
        "element_type",
        "description",
    )
    list_filter = (DesignFilter, ElementTypeFilter, "permanence", "is_risky")
    search_fields = ("name", "design__name", "element_type__name")
    autocomplete_fields = ("design", "element_type")
    readonly_fields = ("tags",)
    inlines = [ElementTagsInline, ElementAttachmentInline]

    def tags(self, obj):
        return ", ".join(map(str, obj.all_tags.all()))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "element_type":
            kwargs["queryset"] = ElementType.objects.not_instance_of(MapElementType)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(MapElement)
class MapElementAdmin(ElementAdmin):
    class Media:
        js = ("designs/admin/map_element.js",)

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
        return [shape_inline, *inlines]

    def json_str_style(self, obj):
        # For map drawing
        return json.dumps(obj.json_style)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            fields = (*fields, "json_str_style")
        return fields
