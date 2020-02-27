from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from ...models.map import Parcel


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ("number", "link_to_project", "insee", "section")

    def link_to_project(self, obj):
        link = reverse("admin:api_project_change", args=[obj.project.id])
        return format_html('<a href="{}">{}</a>', link, obj.project.name)

    link_to_project.short_description = "Project"
