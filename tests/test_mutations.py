import graphene

import graphql_jwt

from . import mutations
from .testcases import GraphQLSchemaTestCase


class VerifyTests(mutations.VerifyTestsMixin, GraphQLSchemaTestCase):

    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()

    def execute(self, variables):
        query = '''
        mutation VerifyToken($token: String!) {
          verifyToken(token: $token) {
            payload
          }
        }'''

        return self.client.execute(query, **variables)


class RefreshTests(mutations.RefreshTestsMixin, GraphQLSchemaTestCase):

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

        return self.client.execute(query, **variables)
