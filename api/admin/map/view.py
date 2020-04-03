from django.contrib import admin

from ..mixins import LinkToProjectMixin
from ...models.map import Feature, View


class FeatureInline(admin.TabularInline):
    model = View.features.through

    def __init__(self, *args, project=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.project = project

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "feature" and self.project is not None:
            kwargs["queryset"] = Feature.objects.filter(project=self.project)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(View)
class ViewAdmin(admin.ModelAdmin, LinkToProjectMixin):
    list_display = ("name", "link_to_project")
    save_on_top = True
    search_fields = ("name", "project__name")

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project")
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        project = obj.project if obj is not None else None
        if project is None:
            return []
        return [FeatureInline(self.model, self.admin_site, project=project)]
