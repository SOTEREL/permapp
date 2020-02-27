from django.contrib import admin

from ..models import Project
from ..models.map import Parcel


class ParcelInline(admin.TabularInline):
    model = Parcel


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        ParcelInline,
    ]
