from django.urls import reverse


def get_instance_url(instance):
    app = instance._meta.app_label
    model = instance._meta.model_name
    return reverse(f"admin:{app}_{model}_change", args=(instance.pk,))


def get_instance_href(instance, val=None, attrs={}):
    url = get_instance_url(instance)
    attrs = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f'<a href="{url}" {attrs}>{val or instance}</a>'
