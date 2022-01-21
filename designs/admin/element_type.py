from admin_auto_filters.filters import AutocompleteFilter
from categories.admin import CategoryBaseAdmin
from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from tagging.models import TaggedItem

from ..models import ElementType, ElementTypeCategory, MapElementType


class CategoryFilter(AutocompleteFilter):
    title = "category"
    field_name = "categories"


class ElementTypeTagsInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ("tag",)


@admin.register(ElementTypeCategory)
class ElementTypeCategoryAdmin(CategoryBaseAdmin):
    autocomplete_fields = ("parent",)


@admin.register(ElementType)
class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    list_filter = (CategoryFilter,)
    search_fields = ("name",)
    inlines = [ElementTypeTagsInline]
    autocomplete_fields = ("categories",)

    def has_module_permission(self, request):
        # Not used for now
        return False


@admin.register(MapElementType)
class MapElementTypeAdmin(ElementTypeAdmin):
    list_display = (
        "name",
        "shape_ctype",
        "description",
    )
    list_filter = (
        CategoryFilter,
        "shape_ctype",
    )
    inlines = [ElementTypeTagsInline]

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
            {
                "model": obj.style_cls,
                "autocomplete_fields": ("map_theme",),
                "formfield_overrides": {
                    models.CharField: {"widget": forms.TextInput(attrs={"size": 5})}
                },
            },
        )
        return [*inlines, style_inline]

    def has_module_permission(self, request):
        return admin.ModelAdmin.has_module_permission(self, request)
