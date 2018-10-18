from calendar import timegm

from django.utils.translation import ugettext as _

import graphene

from .. import exceptions
from ..settings import jwt_settings
from .shortcuts import get_refresh_token


class RefreshTokenMixin(object):

    class Fields:
        refresh_token = graphene.String(required=True)

    @classmethod
    def refresh(cls, root, info, refresh_token, **kwargs):
        context = info.context
        refresh_token = get_refresh_token(refresh_token)

        if refresh_token.is_expired(context):
            raise exceptions.JSONWebTokenError(_('Refresh token is expired'))

        payload = jwt_settings.JWT_PAYLOAD_HANDLER(refresh_token.user, context)
        token = jwt_settings.JWT_ENCODE_HANDLER(payload, context)
        refreshed_token = refresh_token.rotate().token

        return cls(token=token, payload=payload, refresh_token=refreshed_token)


class RevokeMixin(object):
    revoked = graphene.Int()

    @classmethod
    def revoke(cls, root, info, refresh_token, **kwargs):
        refresh_token = get_refresh_token(refresh_token)
        refresh_token.revoke()

        return cls(revoked=timegm(refresh_token.revoked.timetuple()))
