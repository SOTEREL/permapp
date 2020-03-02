from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("_admin/", admin.site.urls),
    path("_api/", include("api.urls")),
    # Must be at the end as it catches all urls (for vue-router)
    path("", include("spa.urls")),
]
