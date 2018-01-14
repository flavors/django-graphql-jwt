import graphene

from . import mutations
from .utils import get_payload

__all__ = ['Verify', 'Refresh']


class JWTMutationMixin(object):

    class Input:
        token = graphene.String()


class Verify(JWTMutationMixin,
             mutations.VerifyMixin,
             graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token))


class Refresh(JWTMutationMixin,
              mutations.RefreshMixin,
              graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.refresh(*args, **kwargs)
