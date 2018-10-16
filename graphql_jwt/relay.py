import graphene

from . import mixins
from .decorators import token_auth
from .utils import get_payload

__all__ = [
    'JSONWebTokenMutation',
    'ObtainJSONWebToken',
    'Verify',
    'Refresh',
]


class JSONWebTokenMutation(mixins.ObtainJSONWebTokenMixin,
                           graphene.ClientIDMutation):

    class Meta:
        abstract = True

    @classmethod
    def Field(cls, *args, **kwargs):
        cls._meta.arguments['input']._meta.fields.update({
            get_user_model().USERNAME_FIELD:
            graphene.InputField(graphene.String, required=True),
            'password': graphene.InputField(graphene.String, required=True),
        })
        return super(JSONWebTokenMutation, cls).Field(*args, **kwargs)

    @classmethod
    @token_auth
    def mutate_and_get_payload(cls, root, info, **kwargs):
        return cls.resolve(root, info)


class ObtainJSONWebToken(mixins.ResolveMixin, JSONWebTokenMutation):
    """Obtain JSON Web Token mutation"""


class JSONWebTokenMixin(object):

    class Input:
        token = graphene.String(required=True)


class Verify(JSONWebTokenMixin,
             mixins.VerifyMixin,
             graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, root, info, token, **kwargs):
        return cls(payload=get_payload(token, info.context))


class Refresh(JSONWebTokenMixin,
              mixins.RefreshMixin,
              graphene.relay.ClientIDMutation):

    @classmethod
    def mutate_and_get_payload(cls, *args, **kwargs):
        return cls.refresh(*args, **kwargs)
