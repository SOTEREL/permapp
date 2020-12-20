from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.html import format_html
from permapp.admin import get_instance_href

from ..models import MapElementType, MapTheme


@admin.register(MapTheme)
class MapThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "styles_html", "missing_styles_html")
    search_fields = ("name",)

    def styles_html(self, obj):
        return format_html(
            ", ".join(
                get_instance_href(style, val=style.map_element_type.name)
                for style in obj.styles.order_by("map_element_type__name")
            )
        )

    styles_html.short_description = "styles"

    def missing_styles_html(self, obj):
        ctype = ContentType.objects.get_for_model(MapElementType)
        add_url = (
            lambda elem_type: reverse(f"admin:{ctype.app_label}_{ctype.model}_add")
            + f"?map_element_type={elem_type.pk}&map_theme={obj.pk}"
        )
        add_link = lambda elem_type: f'<a href="{add_url(elem_type)}">{elem_type}</a>'
        return format_html(
            ", ".join(
                add_link(elem_type) for elem_type in obj.missing_map_element_types
            )
        )

    missing_styles_html.short_description = "undefined styles"
