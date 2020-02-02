import graphene

import graphql_jwt

from ..testcases import RelaySchemaTestCase
from . import mixins
from .relay import Refresh
from .testcases import RelayCookieTestCase


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = '''
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.relay.ObtainJSONWebToken,
    }


class RefreshTokenTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = '''
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'refresh_token': Refresh,
    }


class RevokeTokenTests(mixins.RevokeMixin, RelaySchemaTestCase):
    query = '''
    mutation RevokeToken($input: RevokeInput!) {
      revokeToken(input: $input) {
        revoked
        clientMutationId
      }
    }'''

    class Mutation(graphene.ObjectType):
        revoke_token = graphql_jwt.relay.Revoke.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, RelayCookieTestCase):
    query = '''
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshToken
        refreshExpiresIn
        clientMutationId
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.relay.ObtainJSONWebToken,
    }


class CookieRefreshTests(mixins.CookieRefreshMixin, RelayCookieTestCase):
    query = '''
    mutation {
      refreshToken(input: {}) {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }'''

    refresh_token_mutations = {
        'refresh_token': Refresh,
    }


class DeleteCookieTests(mixins.DeleteCookieMixin, RelayCookieTestCase):
    query = '''
    mutation {
      deleteCookie(input: {}) {
        deleted
      }
    }'''

    class Mutation(graphene.ObjectType):
        delete_cookie = graphql_jwt.relay.DeleteRefreshTokenCookie.Field()
