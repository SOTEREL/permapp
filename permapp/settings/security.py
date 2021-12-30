from .base import DEBUG, read_env

env = read_env()

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = ["*"] if DEBUG else env.list("ALLOWED_HOSTS")

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SECURE_HSTS_SECONDS = 0 if DEBUG else 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = not DEBUG
SECURE_REFERRER_POLICY = "same-origin"  # We need a referer for the CSRF in API mode

AUTH_USER_MODEL = "custom_auth.User"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]
