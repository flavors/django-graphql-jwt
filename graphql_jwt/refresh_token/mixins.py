from calendar import timegm

from django.utils.translation import gettext as _

import graphene

from .. import exceptions
from ..decorators import refresh_expiration, setup_jwt_cookie
from ..settings import jwt_settings
from . import signals
from .decorators import ensure_refresh_token
from .shortcuts import (
    create_refresh_token, get_refresh_token, refresh_token_lazy,
)


class RefreshTokenMixin:

    class Fields:
        refresh_token = graphene.String()

    @classmethod
    @setup_jwt_cookie
    @refresh_expiration
    @ensure_refresh_token
    def refresh(cls, root, info, refresh_token, **kwargs):
        context = info.context
        old_refresh_token = get_refresh_token(refresh_token, context)

        if old_refresh_token.is_expired(context):
            raise exceptions.JSONWebTokenError(_('Refresh token is expired'))

        payload = jwt_settings.JWT_PAYLOAD_HANDLER(
            old_refresh_token.user,
            context,
        )
        token = jwt_settings.JWT_ENCODE_HANDLER(payload, context)

        if getattr(context, 'jwt_cookie', False):
            context.jwt_refresh_token = create_refresh_token(
                old_refresh_token.user,
                old_refresh_token,
            )
            new_refresh_token = context.jwt_refresh_token.get_token()
        else:
            new_refresh_token = refresh_token_lazy(
                old_refresh_token.user,
                old_refresh_token,
            )

        signals.refresh_token_rotated.send(
            sender=cls,
            request=context,
            refresh_token=old_refresh_token,
            refresh_token_issued=new_refresh_token,
        )
        return cls(
            token=token,
            payload=payload,
            refresh_token=new_refresh_token,
        )


class RevokeMixin:
    revoked = graphene.Int(required=True)

    @classmethod
    @ensure_refresh_token
    def revoke(cls, root, info, refresh_token, **kwargs):
        context = info.context
        refresh_token_obj = get_refresh_token(refresh_token, context)
        refresh_token_obj.revoke(context)
        return cls(revoked=timegm(refresh_token_obj.revoked.timetuple()))


class DeleteRefreshTokenCookieMixin:
    deleted = graphene.Boolean(required=True)

    @classmethod
    def delete_cookie(cls, root, info, **kwargs):
        context = info.context
        context.delete_refresh_token_cookie = (
            jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME in context.COOKIES and
            context.jwt_cookie
        )
        return cls(deleted=context.delete_refresh_token_cookie)
