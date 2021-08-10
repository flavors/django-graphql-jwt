import graphene

import graphql_jwt

from . import mixins
from .testcases import RelayCookieTestCase, RelaySchemaTestCase


class TokenAuthTests(mixins.TokenAuthMixin, RelaySchemaTestCase):
    query = """
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()


class VerifyTests(mixins.VerifyMixin, RelaySchemaTestCase):
    query = """
    mutation VerifyToken($input: VerifyInput!) {
      verifyToken(input: $input) {
        payload
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        verify_token = graphql_jwt.relay.Verify.Field()


class RefreshTests(mixins.RefreshMixin, RelaySchemaTestCase):
    query = """
    mutation RefreshToken($input: RefreshInput!) {
      refreshToken(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = graphql_jwt.relay.Refresh.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, RelayCookieTestCase):
    query = """
    mutation TokenAuth($input: ObtainJSONWebTokenInput!) {
      tokenAuth(input: $input) {
        token
        payload
        refreshExpiresIn
        clientMutationId
      }
    }"""

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()


class CookieRefreshTests(mixins.CookieRefreshMixin, RelayCookieTestCase):
    query = """
    mutation {
      refreshToken(input: {}) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = graphql_jwt.relay.Refresh.Field()


class DeleteCookieTests(mixins.DeleteCookieMixin, RelayCookieTestCase):
    query = """
    mutation {
      deleteCookie(input: {}) {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = graphql_jwt.relay.DeleteJSONWebTokenCookie.Field()
