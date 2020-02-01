import graphene

import graphql_jwt

from ..testcases import RelaySchemaTestCase
from . import mixins
from .relay import Refresh


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = '''
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.relay.ObtainJSONWebToken,
    }


class RefreshTokenTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = '''
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
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
