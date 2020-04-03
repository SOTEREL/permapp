from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html

from ..models import Project


class LinkToProject:
    def link_to_project(self, obj):
        ctype = ContentType.objects.get_for_model(Project)
        link = reverse(
            "admin:%s_%s_change" % (ctype.app_label, ctype.model),
            args=(obj.project.id,),
        )
        return format_html('<a href="{}">{}</a>', link, obj.project.name)

    link_to_project.short_description = "project"
