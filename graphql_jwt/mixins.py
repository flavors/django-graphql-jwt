from django.utils.translation import gettext as _

import graphene
from graphene.types.generic import GenericScalar

from . import exceptions, signals
from .decorators import ensure_token, refresh_expiration, setup_jwt_cookie
from .refresh_token.mixins import RefreshTokenMixin
from .settings import jwt_settings
from .utils import get_payload, get_user_by_payload


class JSONWebTokenMixin:
    payload = GenericScalar(required=True)
    refresh_expires_in = graphene.Int(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields['token'] =\
                graphene.Field(graphene.String, required=True)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields['refresh_token'] =\
                    graphene.Field(graphene.String, required=True)

        return super().Field(*args, **kwargs)


class ObtainJSONWebTokenMixin(JSONWebTokenMixin):

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, 'resolve', None), (
            '{name}.resolve method is required in a JSONWebTokenMutation.'
        ).format(name=name or cls.__name__)

        super().__init_subclass_with_meta__(name=name, **options)


class VerifyMixin:
    payload = GenericScalar(required=True)

    @classmethod
    @ensure_token
    def verify(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token, info.context))


class ResolveMixin:

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls()


class KeepAliveRefreshMixin:

    class Fields:
        token = graphene.String()

    @classmethod
    @setup_jwt_cookie
    @refresh_expiration
    @ensure_token
    def refresh(cls, root, info, token, **kwargs):
        context = info.context
        payload = get_payload(token, context)
        user = get_user_by_payload(payload)
        orig_iat = payload.get('origIat')

        if not orig_iat:
            raise exceptions.JSONWebTokenError(_('origIat field is required'))

        if jwt_settings.JWT_REFRESH_EXPIRED_HANDLER(orig_iat, context):
            raise exceptions.JSONWebTokenError(_('Refresh has expired'))

        payload = jwt_settings.JWT_PAYLOAD_HANDLER(user, context)
        payload['origIat'] = orig_iat

        token = jwt_settings.JWT_ENCODE_HANDLER(payload, context)
        signals.token_refreshed.send(sender=cls, request=context, user=user)
        return cls(token=token, payload=payload)


class RefreshMixin((RefreshTokenMixin
                    if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN
                    else KeepAliveRefreshMixin),
                   JSONWebTokenMixin):
    """RefreshMixin"""


class DeleteJSONWebTokenCookieMixin:
    deleted = graphene.Boolean(required=True)

    @classmethod
    def delete_cookie(cls, root, info, **kwargs):
        context = info.context
        context.delete_jwt_cookie = (
            jwt_settings.JWT_COOKIE_NAME in context.COOKIES and
            context.jwt_cookie
        )
        return cls(deleted=context.delete_jwt_cookie)
