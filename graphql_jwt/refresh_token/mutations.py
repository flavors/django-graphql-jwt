import graphene

from . import mixins


class Revoke(mixins.RevokeMixin, graphene.Mutation):
    class Arguments:
        refresh_token = graphene.String()

    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.revoke(*args, **kwargs)


class DeleteRefreshTokenCookie(mixins.DeleteRefreshTokenCookieMixin, graphene.Mutation):
    @classmethod
    def mutate(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)
