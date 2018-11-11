import graphene

import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin

from . import mixins
from ..testcases import RelaySchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = '''
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        refreshToken
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.relay.ObtainJSONWebToken,
    }


class Refresh(RefreshTokenMixin, graphql_jwt.relay.Refresh):

    class Input(RefreshTokenMixin.Fields):
        """Refresh Input"""


class RefreshTokenTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = '''
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        refreshToken
        payload
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'refresh_token': Refresh,
    }


class RevokeTokenTests(mixins.RevokeMixin, RelaySchemaTestCase):
    query = '''
    mutation RevokeToken($input: RevokeInput!) {
      revokeToken(input: $input) {
        revoked
        clientMutationId
      }
    }'''

    class Mutation(graphene.ObjectType):
        revoke_token = graphql_jwt.relay.Revoke.Field()
