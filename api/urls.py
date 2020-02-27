from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"projects", views.ProjectViewSet)
router.register(r"parcels", views.map.ParcelViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
