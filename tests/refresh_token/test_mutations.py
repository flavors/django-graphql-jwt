import graphene

import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin

from ..testcases import SchemaTestCase
from . import mixins


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


class Refresh(RefreshTokenMixin, graphql_jwt.Refresh):

    class Arguments(RefreshTokenMixin.Fields):
        """Refresh Arguments"""


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
