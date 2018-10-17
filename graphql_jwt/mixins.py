from django.utils.translation import ugettext as _

import graphene

from . import exceptions
from .refresh_token.mixins import LongRunningRefreshTokenMixin
from .settings import jwt_settings
from .shortcuts import get_token
from .utils import get_payload, get_user_by_payload


class JSONWebTokenMixin(object):
    token = graphene.String()

    @classmethod
    def Field(cls, *args, **kwargs):
        if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
            cls._meta.fields['refresh_token'] = graphene.Field(graphene.String)

        return super(JSONWebTokenMixin, cls).Field(*args, **kwargs)


class ObtainJSONWebTokenMixin(JSONWebTokenMixin):

    @classmethod
    def __init_subclass_with_meta__(cls, name=None, **options):
        assert getattr(cls, 'resolve', None), (
            '{name}.resolve method is required in a JSONWebTokenMutation.'
        ).format(name=name or cls.__name__)

        super(ObtainJSONWebTokenMixin, cls)\
            .__init_subclass_with_meta__(name=name, **options)


class ResolveMixin(object):

    @classmethod
    def resolve(cls, root, info):
        return cls()


class KeepAliveRefreshMixin(object):

    class Fields:
        token = graphene.String(required=True)

    @classmethod
    def refresh(cls, root, info, token, **kwargs):
        payload = get_payload(token, info.context)
        user = get_user_by_payload(payload)
        orig_iat = payload.get('origIat')

        if not orig_iat:
            raise exceptions.JSONWebTokenError(_('origIat field is required'))

        if jwt_settings.JWT_REFRESH_EXPIRED_HANDLER(orig_iat, info.context):
            raise exceptions.JSONWebTokenError(_('Refresh has expired'))

        token = get_token(user, info.context, origIat=orig_iat)
        return cls(token=token, payload=payload)


class RefreshMixin((LongRunningRefreshTokenMixin
class RefreshMixin((RefreshTokenMixin
                    if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN
                    else KeepAliveRefreshMixin),
                   JSONWebTokenMixin):
    """Refresh mixin"""
