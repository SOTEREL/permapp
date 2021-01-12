from django.contrib import admin

from ..models import LineStyle, PointStyle, PolygonStyle


class MapStyleAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


admin.site.register(LineStyle, MapStyleAdmin)
admin.site.register(PointStyle, MapStyleAdmin)
admin.site.register(PolygonStyle, MapStyleAdmin)
