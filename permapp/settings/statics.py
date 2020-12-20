import os

from django.core.files.storage import FileSystemStorage

from .base import BASE_DIR, read_env

env = read_env()

STATIC_URL = "/static/"
STATIC_ROOT = env.path(
    "COLLECTED_STATIC_DIR", default=os.path.join(BASE_DIR, "collectedstatic")
)

MEDIA_URL = "/media/"
MEDIA_PRIVATE_URL = "/_media/"
MEDIA_ROOT = env.path("MEDIA_DIR", default=os.path.join(BASE_DIR, "media"))
MEDIA_PRIVATE_ROOT = env.path(
    "MEDIA_PRIVATE_DIR", default=os.path.join(BASE_DIR, "media_secret")
)

PRIVATE_FS = FileSystemStorage(
    location=str(MEDIA_PRIVATE_ROOT), base_url=MEDIA_PRIVATE_URL
)
