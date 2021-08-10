from functools import wraps

from django.utils.translation import gettext as _

from .. import exceptions
from ..settings import jwt_settings


def ensure_refresh_token(f):
    @wraps(f)
    def wrapper(cls, root, info, refresh_token=None, *args, **kwargs):
        if refresh_token is None:
            refresh_token = info.context.COOKIES.get(
                jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
            )
            if refresh_token is None:
                raise exceptions.JSONWebTokenError(
                    _("Refresh token is required"),
                )
        return f(cls, root, info, refresh_token, *args, **kwargs)

    return wrapper
