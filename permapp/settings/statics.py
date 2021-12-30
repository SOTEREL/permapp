import os

from django.core.files.storage import FileSystemStorage

from .base import BASE_DIR, DEBUG, read_env

env = read_env()

DJANGO_VITE_DEV_MODE = DEBUG
DJANGO_VITE_ASSETS_PATH = os.path.join(BASE_DIR, "static", "dist")

STATIC_URL = "/static/"
STATIC_ROOT = env.path(
    "COLLECTED_STATIC_DIR", default=os.path.join(BASE_DIR, "collectedstatic")
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static", "assets")]

if os.path.isdir(DJANGO_VITE_ASSETS_PATH):
    STATICFILES_DIRS.append(DJANGO_VITE_ASSETS_PATH)

MEDIA_URL = "/media/"
MEDIA_PRIVATE_URL = "/_media/"
MEDIA_ROOT = env.path("MEDIA_DIR", default=os.path.join(BASE_DIR, "media"))
MEDIA_PRIVATE_ROOT = env.path(
    "MEDIA_PRIVATE_DIR", default=os.path.join(BASE_DIR, "media_secret")
)

PRIVATE_FS = FileSystemStorage(
    location=str(MEDIA_PRIVATE_ROOT), base_url=MEDIA_PRIVATE_URL
)
