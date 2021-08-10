import graphene

from . import mixins


class Revoke(mixins.RevokeMixin, graphene.ClientIDMutation):
    class Input:
        refresh_token = graphene.String()

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.revoke(*args, **kwargs)


class DeleteRefreshTokenCookie(
    mixins.DeleteRefreshTokenCookieMixin,
    graphene.ClientIDMutation,
):
    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.delete_cookie(*args, **kwargs)
