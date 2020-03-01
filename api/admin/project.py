from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from inline_actions.admin import InlineActionsModelAdminMixin

from ..forms import ProjectForm
from ..models import Project
from ..models.map import Parcel


class ParcelInline(admin.TabularInline):
    model = Parcel


@admin.register(Project)
class ProjectAdmin(InlineActionsModelAdminMixin, admin.ModelAdmin):
    form = ProjectForm
    inlines = [ParcelInline]
    save_on_top = True
    search_fields = ("name",)

    def get_inline_actions(self, request, obj=None):
        actions = super().get_inline_actions(request, obj=obj)
        if obj is None:
            return actions

        actions.append("add_parcel")

        return actions

    def get_add_parcel_label(self, obj):
        return "Add parcel"

    def add_parcel(self, request, obj, parent_obj=None):
        return redirect(reverse("admin:api_parcel_add") + f"?project={obj.id}")
