from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig


class CustomAdminSite(AdminSite):
    pass


class CustomAdminConfig(AdminConfig):
    default_site = "design_perma.admin.CustomAdminSite"
