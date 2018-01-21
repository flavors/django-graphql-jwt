import graphene

import graphql_jwt

from . import mixins
from .testcases import GraphQLSchemaTestCase


class ObtainJSONWebTokenTests(mixins.ObtainJSONWebTokenTestsMixin,
                              GraphQLSchemaTestCase):

    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()

    def execute(self, input):
        query = '''
        mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
          tokenAuth(input: $input) {
            token
            clientMutationId
          }
        }'''

        return self.client.execute(query, input=input)


class VerifyTests(mixins.VerifyTestsMixin, GraphQLSchemaTestCase):

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


class RefreshTests(mixins.RefreshTestsMixin, GraphQLSchemaTestCase):

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
