CORS_ORIGIN_WHITELIST = ["http://localhost:8080", "http://127.0.0.1:8080"]

REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"]
}
