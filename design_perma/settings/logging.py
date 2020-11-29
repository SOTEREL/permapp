import os

from .base import BASE_DIR, read_env

env = read_env()

LOGS_DIR = env.path("LOGS_DIR", default=BASE_DIR)
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse",},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue",},
    },
    "formatters": {
        "simple": {
            "format": "[%(asctime)s][%(levelname)s][%(name)s] %(message)s",
            "datefmt": "%d/%b/%Y %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
        },
        "django_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filters": ["require_debug_false"],
            "filename": os.path.join(LOGS_DIR, "django.log"),
            "encoding": "utf-8",
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "simple",
        },
        "cron_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "cron.log"),
            "encoding": "utf-8",
            "maxBytes": 1024 * 1024,  # 1MB
            "backupCount": 3,
            "formatter": "simple",
        },
        "design_perma_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOGS_DIR, "avl_genetics.log"),
            "encoding": "utf-8",
            "maxBytes": 1024 * 1024,  # 1MB
            "backupCount": 3,
            "formatter": "simple",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "simple",
            "include_html": True,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "django_file", "mail_admins"],
            "level": "INFO",
        },
        "design_perma": {
            "handlers": ["console", "design_perma_file", "mail_admins",],
            "level": "INFO",
        },
        "cron": {"handlers": ["cron_file", "mail_admins"], "level": "INFO",},
    },
}
