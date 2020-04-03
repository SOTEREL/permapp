from django.contrib import admin
from django.contrib.admin.helpers import AdminErrorList, AdminForm
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from polymorphic.admin import PolymorphicInlineSupportMixin

from ..mixins import LinkToProject
from ...forms.map import (
    make_feature_change_form,
    make_feature_add_form,
    FeatureAddTypeForm,
    shapes as shape_forms,
)
from ...models.map import Feature, FeatureAttachment, FeatureType


class AttachmentInline(admin.TabularInline):
    model = FeatureAttachment


class BaseFeatureAdmin(PolymorphicInlineSupportMixin, admin.ModelAdmin, LinkToProject):
    add_form = None
    form = make_feature_change_form(Feature)

    list_display = ("link_to_change", "type", "link_to_project", "comments")
    list_display_links = None
    list_filter = ("is_risky", "type__category")
    search_fields = ("name", "comments", "project__name")
    save_on_top = True

    def link_to_change(self, obj):
        ctype = obj.type.feature_ctype
        link = reverse(
            "admin:%s_%s_change" % (ctype.app_label, ctype.model), args=(obj.id,)
        )
        return format_html('<strong><a href="{}">{}</a></strong>', link, obj.name)

    link_to_change.short_description = "name"

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs["form"] = self.add_form
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj is not None:
            return (*readonly_fields, "project", "type")
        return readonly_fields

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            return []

        ShapeInline = type(
            "ShapeInline",
            (admin.StackedInline,),
            {
                "model": obj.shape_model,
                "form": getattr(
                    shape_forms,
                    f"{obj.shape_model.__name__}Form",
                    shape_forms.make_geojson_form(obj.shape_model),
                ),
                "readonly_fields": ["shape_ptr"],
                "can_delete": False,
                "extra": 0,
            },
        )

        return [
            ShapeInline(self.model, self.admin_site),
            AttachmentInline(self.model, self.admin_site),
        ]


@admin.register(Feature)
class FeatureAdmin(BaseFeatureAdmin):
    add_form = make_feature_add_form(Feature)
    add_type_template = "api/admin_add_type_form.html"
    add_type_form = FeatureAddTypeForm

    def get_extra_qs(self, request):
        if request.META["QUERY_STRING"]:
            # QUERY_STRING is bytes in Python 3, using force_text() to decode it as string.
            # See QueryDict how Django deals with that.
            return "&{0}".format(force_text(request.META["QUERY_STRING"]))
        return ""

    def add_view(self, request, form_url="", extra_context=None):
        feature_type = int(request.GET.get("type", 0))
        if not feature_type:
            return self.add_type_view(request)

        feature_type = get_object_or_404(FeatureType, pk=feature_type)
        if feature_type.feature_model is not Feature:
            ctype = feature_type.feature_ctype
            base_url = reverse("admin:%s_%s_add" % (ctype.app_label, ctype.model))
            extra_qs = self.get_extra_qs(request)
            return HttpResponseRedirect(f"{base_url}?{extra_qs}")

        return super().add_view(request, form_url="", extra_context=None)

    def add_type_view(self, request, form_url=""):
        if not self.has_add_permission(request):
            raise PermissionDenied

        extra_qs = self.get_extra_qs(request)
        form = self.add_type_form(
            data=request.POST if request.method == "POST" else None
        )

        if form.is_valid():
            return HttpResponseRedirect(
                "?type={0}{1}".format(form.cleaned_data["type"].pk, extra_qs)
            )

        # Wrap in all admin layout
        fieldsets = ((None, {"fields": ("type",)}),)
        admin_form = AdminForm(form, fieldsets, {}, model_admin=self)
        media = self.media + admin_form.media
        opts = self.model._meta

        context = {
            "title": _("Add %s") % force_text(opts.verbose_name),
            "adminform": admin_form,
            "is_popup": ("_popup" in request.POST or "_popup" in request.GET),
            "media": mark_safe(media),
            "errors": AdminErrorList(form, ()),
            "app_label": opts.app_label,
            "has_change_permission": self.has_change_permission(request),
            "form_url": mark_safe(form_url),
            "opts": opts,
            "add": True,
            "save_on_top": self.save_on_top,
        }

        request.current_app = self.admin_site.name
        return TemplateResponse(request, self.add_type_template, context)
