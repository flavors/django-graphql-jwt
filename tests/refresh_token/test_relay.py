import graphene

import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin

from . import mixins
from ..decorators import input_variables
from ..testcases import SchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    refresh_token_mutations = {
        'token_auth': graphql_jwt.relay.ObtainJSONWebToken,
    }

    @input_variables
    def execute(self, variables):
        query = '''
        mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
          tokenAuth(input: $input) {
            token
            refreshToken
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables)


class Refresh(RefreshTokenMixin, graphql_jwt.relay.Refresh):

    class Input(RefreshTokenMixin.Fields):
        """Refresh Input"""


class RefreshTokenTests(mixins.RefreshMixin, SchemaTestCase):
    refresh_token_mutations = {
        'refresh_token': Refresh,
    }

    @input_variables
    def execute(self, variables):
        query = '''
        mutation RefreshToken($input: RefreshInput!) {
          refreshToken(input: $input) {
            token
            refreshToken
            payload
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables)


class RevokeTokenTests(mixins.RevokeMixin, SchemaTestCase):

    class Mutations(graphene.ObjectType):
        revoke_token = graphql_jwt.relay.Revoke.Field()

    @input_variables
    def execute(self, variables):
        query = '''
        mutation RevokeToken($input: RevokeInput!) {
          revokeToken(input: $input) {
            revoked
            clientMutationId
          }
        }'''

        return self.client.execute(query, variables)
