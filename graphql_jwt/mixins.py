from django.utils.translation import gettext as _

import graphene
from graphene.types.generic import GenericScalar
from graphene.utils.thenables import maybe_thenable

from . import exceptions, signals
from .decorators import csrf_rotation, ensure_token, setup_jwt_cookie
from .refresh_token.mixins import RefreshTokenMixin
from .settings import jwt_settings
from .utils import get_payload, get_user_by_payload


class JSONWebTokenMixin:
    payload = GenericScalar(required=True)
    refresh_expires_in = graphene.Int(required=True)

    @classmethod
    def Field(cls, *args, **kwargs):
        if not jwt_settings.JWT_HIDE_TOKEN_FIELDS:
            cls._meta.fields["token"] = graphene.Field(graphene.String, required=True)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                cls._meta.fields["refresh_token"] = graphene.Field(
                    graphene.String,
                    required=True,
                )

        return super().Field(*args, **kwargs)


class ObtainJSONWebTokenMixin(JSONWebTokenMixin):
    @classmethod
    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, "resolve", None), (
            f"{name or cls.__name__}.resolve "
            "method is required in a JSONWebTokenMutation."
        )

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
    @csrf_rotation
    @ensure_token
    def refresh(cls, root, info, token, **kwargs):
        def on_resolve(values):
            payload, token = values
            payload.token = token
            return payload

        context = info.context
        payload = get_payload(token, context)
        user = get_user_by_payload(payload)
        orig_iat = payload.get("origIat")

        if not orig_iat:
            raise exceptions.JSONWebTokenError(_("origIat field is required"))

        if jwt_settings.JWT_REFRESH_EXPIRED_HANDLER(orig_iat, context):
            raise exceptions.JSONWebTokenError(_("Refresh has expired"))

        payload = jwt_settings.JWT_PAYLOAD_HANDLER(user, context)
        payload["origIat"] = orig_iat
        refresh_expires_in = (
            orig_iat + jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
        )

        token = jwt_settings.JWT_ENCODE_HANDLER(payload, context)
        signals.token_refreshed.send(sender=cls, request=context, user=user)

        result = cls(payload=payload, refresh_expires_in=refresh_expires_in)
        return maybe_thenable((result, token), on_resolve)


class RefreshMixin(
    (
        RefreshTokenMixin
        if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN
        else KeepAliveRefreshMixin
    ),
    JSONWebTokenMixin,
):
    """RefreshMixin"""


class DeleteJSONWebTokenCookieMixin:
    deleted = graphene.Boolean(required=True)

    @classmethod
    def delete_cookie(cls, root, info, **kwargs):
        context = info.context
        context.delete_jwt_cookie = (
            jwt_settings.JWT_COOKIE_NAME in context.COOKIES
            and getattr(context, "jwt_cookie", False)
        )
        return cls(deleted=context.delete_jwt_cookie)
