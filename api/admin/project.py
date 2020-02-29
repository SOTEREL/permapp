from django.contrib import admin

from ..forms import ProjectForm
from ..models import Project
from ..models.map import Parcel


class ParcelInline(admin.TabularInline):
    model = Parcel


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectForm
    inlines = [ParcelInline]
