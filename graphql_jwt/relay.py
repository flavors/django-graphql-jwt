import graphene

from . import mixins
from .utils import get_payload

__all__ = ['Verify', 'Refresh']


class JWTMutationMixin(object):

    class Input:
        token = graphene.String()


class Verify(JWTMutationMixin,
             mixins.VerifyMixin,
             graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token))


class Refresh(JWTMutationMixin,
              mixins.RefreshMixin,
              graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.refresh(*args, **kwargs)
