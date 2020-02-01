import graphene

import graphql_jwt

from . import mixins
from .testcases import SchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    query = '''
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }'''

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()


class VerifyTests(mixins.VerifyMixin, SchemaTestCase):
    query = '''
    mutation VerifyToken($token: String!) {
      verifyToken(token: $token) {
        payload
      }
    }'''

    class Mutation(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    query = '''
    mutation RefreshToken($token: String!) {
      refreshToken(token: $token) {
        token
        payload
        refreshExpiresIn
      }
    }'''

    class Mutation(graphene.ObjectType):
        refresh_token = graphql_jwt.Refresh.Field()
