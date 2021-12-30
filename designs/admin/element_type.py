from django import forms
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from tagging.models import TaggedItem

from ..models import ElementType, MapElementType


class ElementTypeTagsInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ("tag",)


@admin.register(ElementType)
class ElementTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "tags")
    search_fields = ("name",)
    inlines = [ElementTypeTagsInline]

    def tags(self, obj):
        return ", ".join(map(str, obj.tags.all()))

    def has_module_permission(self, request):
        # Not used for now
        return False


@admin.register(MapElementType)
class MapElementTypeAdmin(ElementTypeAdmin):
    list_display = (
        "name",
        "shape_ctype",
        "description",
        "tags",
    )
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
