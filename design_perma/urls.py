from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("_admin/", admin.site.urls),
    path("_api/", include("api.urls")),
    # Will work in dev mode only
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    # Must be at the end as it catches all urls (for vue-router)
    path("", include("spa.urls")),
]
