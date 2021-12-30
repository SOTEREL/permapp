from django.urls import path

from . import views

urlpatterns = [
    path("", views.DesignListView.as_view(), name="design_list",),
    path("<int:pk>/carte/", views.DesignMapView.as_view(), name="design_view_map",),
]
