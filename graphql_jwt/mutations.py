from django.contrib.auth import get_user_model

import graphene

from . import mixins
from .decorators import token_auth
from .refresh_token.mutations import DeleteRefreshTokenCookie, Revoke

__all__ = [
    "JSONWebTokenMutation",
    "ObtainJSONWebToken",
    "Verify",
    "Refresh",
    "Revoke",
    "DeleteRefreshTokenCookie",
]


class JSONWebTokenMutation(mixins.ObtainJSONWebTokenMixin, graphene.Mutation):
    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments.update(
            {
                get_user_model().USERNAME_FIELD: graphene.String(required=True),
                "password": graphene.String(required=True),
            },
        )
        return super().Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate(cls, root, info, **kwargs):
        return cls.resolve(root, info, **kwargs)


class ObtainJSONWebToken(mixins.ResolveMixin, JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""


class Verify(mixins.VerifyMixin, graphene.Mutation):
    class Arguments:
        token = graphene.String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.verify(*args, **kwargs)


class Refresh(mixins.RefreshMixin, graphene.Mutation):
    class Arguments(mixins.RefreshMixin.Fields):
        """Refresh Arguments"""

    @classmethod
    def mutate(cls, *arg, **kwargs):
        return cls.refresh(*arg, **kwargs)


class DeleteJSONWebTokenCookie(mixins.DeleteJSONWebTokenCookieMixin, graphene.Mutation):
    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)
