import graphene

import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin

from . import mixins
from ..testcases import SchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    refresh_token_mutations = {
        'token_auth': graphql_jwt.ObtainJSONWebToken,
    }

    def execute(self, variables):
        query = '''
        mutation TokenAuth($username: String!, $password: String!) {
          tokenAuth(username: $username, password: $password) {
            token
            refreshToken
          }
        }'''

        return self.client.execute(query, variables)


class Refresh(RefreshTokenMixin, graphql_jwt.Refresh):

    class Arguments(RefreshTokenMixin.Fields):
        """Refresh Arguments"""


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    refresh_token_mutations = {
        'refresh_token': Refresh,
    }

    def execute(self, variables):
        query = '''
        mutation RefreshToken($refreshToken: String!) {
          refreshToken(refreshToken: $refreshToken) {
            token
            refreshToken
            payload
          }
        }'''

        return self.client.execute(query, variables)


class RevokeTests(mixins.RevokeMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        revoke_token = graphql_jwt.Revoke.Field()

    def execute(self, variables):
        query = '''
        mutation RevokeToken($refreshToken: String!) {
          revokeToken(refreshToken: $refreshToken) {
            revoked
          }
        }'''

        return self.client.execute(query, variables)
