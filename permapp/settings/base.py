import os

import environ
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.core.validators import EmailValidator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENV_PATH = os.path.join(BASE_DIR, ".env")


def raise_env_error(varname, msg):
    raise ImproperlyConfigured(f"Configuration error for {ENV_PATH}:{varname} : {msg}")


def validate_env_email(email, varname):
    try:
        EmailValidator()(email)
    except ValidationError:
        raise_env_error(varname, f"{email} is an invalid email")


def read_env(*args, **kwargs):
    env = environ.Env(*args, **kwargs)
    env.read_env(ENV_PATH)
    return env


env = read_env()


DEBUG = env.bool("DEBUG")

INSTALLED_APPS = [
    "permapp.admin.CustomAdminConfig",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "debug_toolbar",
    "admin_reorder",
    "rest_framework",
    "martor",
    "admin_auto_filters",
    "django_filters",
    "categories.editor",
    "inline_actions",
    "django_json_widget",
    "jsonschemaform",
    "polymorphic",
    "solo",
    "tagging",
    "colorfield",
    "leaflet",
    "djgeojson",
    "custom_auth",
    "designs",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "admin_reorder.middleware.ModelAdminReorder",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "permapp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "permapp.wsgi.application"
