from functools import wraps

import graphene

import graphql_jwt

from . import mixins
from .testcases import SchemaTestCase


def input_variables(f):
    @wraps(f)
    def wrapper(self, variables):
        return f(self, {'input': variables})
    return wrapper


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()

    @input_variables
    def execute(self, variables):
        query = '''
        mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
          tokenAuth(input: $input) {
            token
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables=variables)


class VerifyTests(mixins.VerifyMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.relay.Verify.Field()

    @input_variables
    def execute(self, variables):
        query = '''
        mutation VerifyToken($input: VerifyInput!) {
          verifyToken(input: $input) {
            payload
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables=variables)


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        refresh_token = graphql_jwt.relay.Refresh.Field()

    @input_variables
    def execute(self, variables):
        query = '''
        mutation RefreshToken($input: RefreshInput!) {
          refreshToken(input: $input) {
            token
            payload
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables=variables)
