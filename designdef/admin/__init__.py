from admin_auto_filters.filters import AutocompleteFilter
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from permapp.admin import get_instance_href
from tagging.models import TaggedItem

from ..models import *  # noqa


class ThemeFilter(AutocompleteFilter):
    title = "theme"
    field_name = "theme"


class ElementTypeFilter(AutocompleteFilter):
    title = "element type"
    field_name = "element_type"


@admin.register(Theme)  # noqa: F405
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "element_types_html", "missing_element_types_html")
    search_fields = ("name",)

    def element_types_html(self, obj):
        return "TODO"
        return format_html(
            ", ".join(
                get_instance_href(
                    themed_elem_type, val=themed_elem_type.element_type.name
                )
                for themed_elem_type in obj.themedelementtype_set.order_by(
                    "element_type__name"
                )
            )
        )

    element_types_html.short_description = "styles"

    def missing_element_types_html(self, obj):
        return "TODO"
        ctype = ContentType.objects.get_for_model(ThemedElementType)  # noqa: F405
        add_url = (
            lambda elem_type: reverse(f"admin:{ctype.app_label}_{ctype.model}_add")
            + f"?element_type={elem_type.pk}&theme={obj.pk}"
        )
        add_link = lambda elem_type: f'<a href="{add_url(elem_type)}">{elem_type}</a>'
        return format_html(
            ", ".join(add_link(elem_type) for elem_type in obj.missing_element_types)
        )

    missing_element_types_html.short_description = "undefined styles"


class ElementTypeTagsInline(GenericTabularInline):
    model = TaggedItem


@admin.register(ElementType)  # noqa: F405
class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "needs", "contributions", "tags")
    search_fields = ("name",)
    inlines = [ElementTypeTagsInline]

    def tags(self, obj):
        return ", ".join(obj.tags.all())


@admin.register(MapElementType)  # noqa: F405
class MapElementTypeAdmin(ElementTypeAdmin):
    inlines = [ElementTypeTagsInline]

    def shape_model(self, obj):
        return obj.shape_cls.__name__

    shape_model.short_description = "shape"
    shape_model.admin_order_field = "shape_ctype"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shape_ctype":
            kwargs["queryset"] = MapElementType.list_usable_shape_ctypes(  # noqa: F405
                as_queryset=True
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            fields = (*fields, "shape_ctype")
        return fields

    def get_inlines(self, request, obj):
        if obj is None:
            return []
        inlines = super().get_inlines(request, obj)
        style_inline = type(
            "MapElementStyleInline",
            (admin.TabularInline,),
            {"model": obj.style_cls, "autocomplete_fields": ("theme",)},
        )
        return [*inlines, style_inline]
