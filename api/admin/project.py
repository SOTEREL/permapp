from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import redirect
from django.urls import reverse

from inline_actions.admin import InlineActionsModelAdminMixin

from ..forms import ProjectForm
from ..models import Project
from ..models.map import Parcel, Feature


@admin.register(Project)
class ProjectAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    form = ProjectForm
    save_on_top = True
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

    def get_inline_actions(self, request, obj=None):
        actions = super().get_inline_actions(request, obj=obj)
        if obj is None:
            return actions

        actions.append("add_parcel")
        actions.append("add_feature")

        return actions

    def redirect_to_add_model(self, project_id, model):
        ctype = ContentType.objects.get_for_model(model)
        return redirect(
            reverse("admin:%s_%s_add" % (ctype.app_label, ctype.model))
            + f"?project={project_id}"
        )

    def get_add_parcel_label(self, obj):
        return "Add parcel"

    def add_parcel(self, request, obj, parent_obj=None):
        return self.redirect_to_add_model(obj.id, Parcel)

    def get_add_feature_label(self, obj):
        return "Add feature"

    def add_feature(self, request, obj, parent_obj=None):
        return self.redirect_to_add_model(obj.id, Feature)
