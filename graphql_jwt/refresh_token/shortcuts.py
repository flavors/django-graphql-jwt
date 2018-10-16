from django.apps import apps
from django.utils.translation import ugettext as _

from ..exceptions import JSONWebTokenError
from ..settings import jwt_settings


def get_refresh_token_model():
    return apps.get_model(jwt_settings.JWT_REFRESH_TOKEN_MODEL)


def get_refresh_token(token):
    RefreshToken = get_refresh_token_model()

    try:
        return RefreshToken.objects.get(token=token, revoked__isnull=True)
    except RefreshToken.DoesNotExist:
        raise JSONWebTokenError(_('Invalid refresh token'))


def create_refresh_token(user):
    return get_refresh_token_model().objects.create(user=user)
