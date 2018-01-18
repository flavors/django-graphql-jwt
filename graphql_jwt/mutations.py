import graphene

from . import mixins
from .utils import get_payload

__all__ = ['Verify', 'Refresh']


class JWTMutationMixin(object):

    class Arguments:
        token = graphene.String()


class Verify(JWTMutationMixin, mixins.VerifyMixin, graphene.Mutation):

    @classmethod
    def mutate(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token))


class Refresh(JWTMutationMixin, mixins.RefreshMixin, graphene.Mutation):

    @classmethod
    def mutate(cls, *arg, **kwargs):
        return cls.refresh(*arg, **kwargs)
