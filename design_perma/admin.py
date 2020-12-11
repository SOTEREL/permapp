from django.contrib.admin import AdminSite
from django.contrib.admin.apps import AdminConfig
from django.urls import reverse


class CustomAdminSite(AdminSite):
    pass


class CustomAdminConfig(AdminConfig):
    default_site = "design_perma.admin.CustomAdminSite"


def get_instance_url(instance):
    app = instance._meta.app_label
    model = instance._meta.model_name
    return reverse(f"admin:{app}_{model}_change", args=(instance.pk,))


def get_instance_href(instance, val=None):
    url = get_instance_url(instance)
    return f'<a href="{url}">{val or instance}</a>'
