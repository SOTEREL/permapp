from .base import read_env


env = read_env()

DEFAULT_DB = env.db()

if DEFAULT_DB["ENGINE"] == "django.db.backends.mysql":
    DEFAULT_DB["OPTIONS"] = {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"}

DATABASES = {"default": DEFAULT_DB}
