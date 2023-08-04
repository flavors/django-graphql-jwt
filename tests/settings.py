INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
    },
}

SECRET_KEY = "test"
USE_TZ = True

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "graphql_jwt.backends.JSONWebTokenBackend",
]

GRAPHENE = {
    "MIDDLEWARE": ["graphql_jwt.middleware.JSONWebTokenMiddleware"],
}
