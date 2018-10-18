import graphene

import graphql_jwt

from . import mixins
from .testcases import SchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    def execute(self, variables):
        query = '''
        mutation TokenAuth($username: String!, $password: String!) {
          tokenAuth(username: $username, password: $password) {
            token
          }
        }'''

        return self.client.execute(query, variables)


class VerifyTests(mixins.VerifyMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()

    def execute(self, variables):
        query = '''
        mutation VerifyToken($token: String!) {
          verifyToken(token: $token) {
            payload
          }
        }'''

        return self.client.execute(query, variables)


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        refresh_token = graphql_jwt.Refresh.Field()

    def execute(self, variables):
        query = '''
        mutation RefreshToken($token: String!) {
          refreshToken(token: $token) {
            token
            payload
          }
        }'''

        return self.client.execute(query, variables)
