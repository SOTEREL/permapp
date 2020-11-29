from django.utils.translation import gettext_lazy as _


LANGUAGE_CODE = "fr-fr"

LANGUAGES = (
    ("fr", _("Français")),
    ("en", _("Anglais")),
)

TIME_ZONE = "Europe/Paris"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "d b. Y"
