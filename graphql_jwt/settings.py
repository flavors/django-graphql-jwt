from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test.signals import setting_changed
from django.utils.module_loading import import_string

DEFAULTS = {
    "JWT_ALGORITHM": "HS256",
    "JWT_AUDIENCE": None,
    "JWT_ISSUER": None,
    "JWT_LEEWAY": 0,
    "JWT_SECRET_KEY": settings.SECRET_KEY,
    "JWT_PUBLIC_KEY": None,
    "JWT_PRIVATE_KEY": None,
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": False,
    "JWT_EXPIRATION_DELTA": timedelta(seconds=60 * 5),
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_LONG_RUNNING_REFRESH_TOKEN": False,
    "JWT_REFRESH_TOKEN_MODEL": "refresh_token.RefreshToken",
    "JWT_REFRESH_TOKEN_N_BYTES": 20,
    "JWT_REUSE_REFRESH_TOKENS": False,
    "JWT_AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "JWT_AUTH_HEADER_PREFIX": "JWT",
    "JWT_ALLOW_ARGUMENT": False,
    "JWT_ARGUMENT_NAME": "token",
    "JWT_ENCODE_HANDLER": "graphql_jwt.utils.jwt_encode",
    "JWT_DECODE_HANDLER": "graphql_jwt.utils.jwt_decode",
    "JWT_PAYLOAD_HANDLER": "graphql_jwt.utils.jwt_payload",
    "JWT_PAYLOAD_GET_USERNAME_HANDLER": (
        lambda payload: payload.get(get_user_model().USERNAME_FIELD)
    ),
    "JWT_GET_USER_BY_NATURAL_KEY_HANDLER": "graphql_jwt.utils.get_user_by_natural_key",
    "JWT_REFRESH_EXPIRED_HANDLER": "graphql_jwt.utils.refresh_has_expired",
    "JWT_GET_REFRESH_TOKEN_HANDLER": (
        "graphql_jwt.refresh_token.utils.get_refresh_token_by_model"
    ),
    "JWT_ALLOW_ANY_HANDLER": "graphql_jwt.middleware.allow_any",
    "JWT_ALLOW_ANY_CLASSES": (),
    "JWT_CSRF_ROTATION": False,
    "JWT_HIDE_TOKEN_FIELDS": False,
    "JWT_COOKIE_NAME": "JWT",
    "JWT_REFRESH_TOKEN_COOKIE_NAME": "JWT-refresh-token",
    "JWT_COOKIE_SECURE": False,
    "JWT_COOKIE_PATH": "/",
    "JWT_COOKIE_DOMAIN": None,
    "JWT_COOKIE_SAMESITE": None,
}

IMPORT_STRINGS = (
    "JWT_ENCODE_HANDLER",
    "JWT_DECODE_HANDLER",
    "JWT_PAYLOAD_HANDLER",
    "JWT_PAYLOAD_GET_USERNAME_HANDLER",
    "JWT_GET_USER_BY_NATURAL_KEY_HANDLER",
    "JWT_REFRESH_EXPIRED_HANDLER",
    "JWT_GET_REFRESH_TOKEN_HANDLER",
    "JWT_ALLOW_ANY_HANDLER",
    "JWT_ALLOW_ANY_CLASSES",
)


def perform_import(value, setting_name):
    if isinstance(value, str):
        return import_from_string(value, setting_name)
    if isinstance(value, (list, tuple)):
        return [import_from_string(item, setting_name) for item in value]
    return value


def import_from_string(value, setting_name):
    try:
        return import_string(value)
    except ImportError as e:
        msg = (
            f"Could not import `{value}` for JWT setting `{setting_name}`."
            f"{e.__class__.__name__}: {e}."
        )
        raise ImportError(msg)


class JWTSettings:
    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError(f"Invalid setting: `{attr}`")

        value = self.user_settings.get(attr, self.defaults[attr])

        if attr == "JWT_ALLOW_ANY_CLASSES":
            value = list(value) + [
                "graphql_jwt.mixins.JSONWebTokenMixin",
                "graphql_jwt.mixins.VerifyMixin",
                "graphql_jwt.refresh_token.mixins.RevokeMixin",
            ]

        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def user_settings(self):
        if not hasattr(self, "_user_settings"):
            self._user_settings = getattr(settings, "GRAPHQL_JWT", {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, "_user_settings"):
            delattr(self, "_user_settings")


def reload_settings(*args, **kwargs):
    setting = kwargs["setting"]

    if setting == "GRAPHQL_JWT":
        jwt_settings.reload()


setting_changed.connect(reload_settings)

jwt_settings = JWTSettings(DEFAULTS, IMPORT_STRINGS)
