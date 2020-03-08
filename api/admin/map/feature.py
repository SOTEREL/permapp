from django.contrib import admin

from ..mixins import LinkToProject
from ...forms.map import make_feature_form
from ...models.map import Feature


class CategoryInlineAdmin(admin.TabularInline):
    model = Feature.categories.through


class FeatureAbstractAdmin(admin.ModelAdmin, LinkToProject):
    list_display = (
        "name",
        "link_to_project",
        "description",
        "permanence",
        "joined_categories",
    )
    list_filter = ("is_observation", "is_important", "categories")
    save_on_top = True
    search_fields = ("name", "description", "project__name", "categories__name")
    inlines = [CategoryInlineAdmin]

    def joined_categories(self, obj):
        cats = obj.categories.values_list("name", flat=True)
        return ", ".join(cats)

    joined_categories.short_description = "categories"

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields


def register_feature_admin(model, **kwargs):
    @admin.register(model)
    class FeatureAdmin(FeatureAbstractAdmin):
        form = make_feature_form(model, **kwargs)
