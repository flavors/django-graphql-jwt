import graphene

import graphql_jwt

from . import mutations
from .testcases import GraphQLSchemaTestCase


class VerifyRelayTests(mutations.VerifyTestsMixin, GraphQLSchemaTestCase):

    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.relay.Verify.Field()

    def execute(self, input):
        query = '''
        mutation VerifyToken($input: VerifyInput!) {
          verifyToken(input: $input) {
            payload
            clientMutationId
          }
        }'''

        return self.client.execute(query, input=input)


class RefreshRelayTests(mutations.RefreshTestsMixin, GraphQLSchemaTestCase):

    class Mutations(graphene.ObjectType):
        refresh_token = graphql_jwt.relay.Refresh.Field()

    def execute(self, input):
        query = '''
        mutation RefreshToken($input: RefreshInput!) {
          refreshToken(input: $input) {
            token
            payload
            clientMutationId
          }
        }'''

        return self.client.execute(query, input=input)
