from django.contrib import admin
from django.utils.html import format_html
from permapp.utils.admin import get_instance_href

from ..models import MapTheme


@admin.register(MapTheme)
class MapThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    readonly_fields = ("styles_html",)

    def styles_html(self, obj):
        return format_html(
            ", ".join(
                get_instance_href(
                    style, val=style.map_element_type.name, attrs={"target": "_blank"}
                )
                for style in obj.styles.order_by("map_element_type__name")
            )
        )

    styles_html.short_description = "styles"
