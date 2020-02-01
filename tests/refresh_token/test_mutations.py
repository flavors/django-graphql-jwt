import graphene

import graphql_jwt

from ..testcases import SchemaTestCase
from . import mixins
from .mutations import Refresh


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    query = '''
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        refreshToken
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.ObtainJSONWebToken,
    }


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    query = '''
    mutation RefreshToken($refreshToken: String!) {
      refreshToken(refreshToken: $refreshToken) {
        token
        refreshToken
        payload
      }
    }'''

    refresh_token_mutations = {
        'refresh_token': Refresh,
    }


class RevokeTests(mixins.RevokeMixin, SchemaTestCase):
    query = '''
    mutation RevokeToken($refreshToken: String!) {
      revokeToken(refreshToken: $refreshToken) {
        revoked
      }
    }'''

    class Mutation(graphene.ObjectType):
        revoke_token = graphql_jwt.Revoke.Field()
