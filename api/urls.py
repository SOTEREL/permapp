from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register("projects", views.ProjectViewSet)
# router.register("parcels", views.map.ParcelViewSet)

map_router = DefaultRouter()
map_router.register("categories", views.map.CategoryViewSet)
map_router.register("features", views.map.FeatureViewSet)
map_router.register("feature_types", views.map.FeatureTypeViewSet)
map_router.register("views", views.map.ViewViewSet)

urlpatterns = [path("", include(router.urls)), path("map/", include(map_router.urls))]
