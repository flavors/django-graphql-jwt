from django.utils.functional import lazy
from django.utils.translation import gettext as _

from ..exceptions import JSONWebTokenError
from ..settings import jwt_settings
from .utils import get_refresh_token_model


def get_refresh_token(token, context=None):
    RefreshToken = get_refresh_token_model()

    try:
        return jwt_settings.JWT_GET_REFRESH_TOKEN_HANDLER(
            refresh_token_model=RefreshToken,
            token=token,
            context=context,
        )

    except RefreshToken.DoesNotExist:
        raise JSONWebTokenError(_("Invalid refresh token"))


def create_refresh_token(user, refresh_token=None):
    if refresh_token is not None and jwt_settings.JWT_REUSE_REFRESH_TOKENS:
        refresh_token.reuse()
        return refresh_token
    return get_refresh_token_model().objects.create(user=user)


refresh_token_lazy = lazy(
    lambda user, refresh_token=None: create_refresh_token(
        user,
        refresh_token,
    ).get_token(),
    str,
)
