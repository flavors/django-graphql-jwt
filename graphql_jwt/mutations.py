from django.contrib.auth import get_user_model

import graphene

from . import mixins
from .decorators import token_auth
from .exceptions import JSONWebTokenError
from .refresh_token.blacklist import is_in_blacklist
from .refresh_token.mutations import Revoke
from .settings import jwt_settings
from .utils import get_payload

__all__ = [
    'JSONWebTokenMutation',
    'ObtainJSONWebToken',
    'Verify',
    'Refresh',
    'Revoke',
]


class JSONWebTokenMutation(mixins.ObtainJSONWebTokenMixin,
                           graphene.Mutation):

    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update({
            get_user_model().USERNAME_FIELD: graphene.String(required=True),
            'password': graphene.String(required=True),
        })
        return super(JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


class ObtainJSONWebToken(mixins.ResolveMixin, JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""


class Verify(mixins.VerifyMixin, graphene.Mutation):

    class Arguments:
        token = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, token, **kwargs):
        payload = get_payload(token, info.context)
        if (
            jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN and
            is_in_blacklist(payload['refresh_token'])
        ):
            raise JSONWebTokenError('Invalid')
        return cls(payload=payload)


class Refresh(mixins.RefreshMixin, graphene.Mutation):

    class Arguments(mixins.RefreshMixin.Fields):
        """Refresh Arguments"""

    @classmethod
    def mutate(cls, *arg, **kwargs):
        return cls.refresh(*arg, **kwargs)
