from admin_auto_filters.filters import AutocompleteFilter
from design_perma.admin import get_instance_href
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from polymorphic.admin import PolymorphicInlineSupportMixin, StackedPolymorphicInline
from tagging.models import TaggedItem

from ..models import *  # noqa


class ElementTypeStyleInline(StackedPolymorphicInline):
    class CircleStyleInline(StackedPolymorphicInline.Child):
        model = CircleStyle  # noqa: F405

    class LineStyleInline(StackedPolymorphicInline.Child):
        model = LineStyle  # noqa: F405

    class PointStyleInline(StackedPolymorphicInline.Child):
        model = PointStyle  # noqa: F405

    class PolygonStyleInline(StackedPolymorphicInline.Child):
        model = PolygonStyle  # noqa: F405

    model = ElementTypeStyle  # noqa: F405
    child_inlines = (
        CircleStyleInline,
        LineStyleInline,
        PointStyleInline,
        PolygonStyleInline,
    )


class ThemeFilter(AutocompleteFilter):
    title = "theme"
    field_name = "theme"


class ElementTypeFilter(AutocompleteFilter):
    title = "element type"
    field_name = "element_type"


@admin.register(ThemedElementType)  # noqa: F405
class ThemedElementTypeAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin):
    list_display = ("element_type", "theme", "shape_model")
    list_filter = (ThemeFilter, ElementTypeFilter)
    search_fields = ("element_type", "theme")
    autocomplete_fields = ("theme", "element_type")
    inlines = [ElementTypeStyleInline]

    def shape_model(self, obj):
        return obj.shape_cls.__name__

    shape_model.short_description = "shape"
    shape_model.admin_order_field = "shape_ctype"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "shape_ctype":
            kwargs[
                "queryset"
            ] = ThemedElementType.list_usable_shape_ctypes(  # noqa: F405
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
        return super().get_inlines(request, obj)


@admin.register(Theme)  # noqa: F405
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "element_types_html", "missing_element_types_html")
    search_fields = ("name",)

    def element_types_html(self, obj):
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
