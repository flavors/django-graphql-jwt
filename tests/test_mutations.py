from django.test import override_settings

import graphene

import graphql_jwt
from graphql_jwt.settings import jwt_settings
from graphql_jwt.signals import token_issued

from . import mixins
from .context_managers import catch_signal
from .testcases import CookieTestCase, SchemaTestCase

GRAPHENE_MODIFIED_SETTINGS = jwt_settings
GRAPHENE_MODIFIED_SETTINGS["JWT_MUTATION_USERNAME_FIELD"] = ["cellphone"]


class TokenAuthTests(mixins.TokenAuthMixin, SchemaTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    def test_token_auth(self):
        with catch_signal(token_issued) as token_issued_handler:
            response = self.execute(
                {
                    self.user.USERNAME_FIELD: self.user.get_username(),
                    "password": "dolphins",
                }
            )

        data = response.data["tokenAuth"]

        self.assertEqual(token_issued_handler.call_count, 1)

        self.assertIsNone(response.errors)
        self.assertUsernameIn(data["payload"])

    @override_settings(GRAPHENE=GRAPHENE_MODIFIED_SETTINGS)
    def test_token_auth_with_custom_username_field(self):
        with catch_signal(token_issued) as token_issued_handler:
            response = self.execute(
                {
                    jwt_settings.JWT_MUTATION_USERNAME_FIELD: self.user.get_username(),
                    "password": "dolphins",
                }
            )

        data = response.data["tokenAuth"]

        self.assertEqual(token_issued_handler.call_count, 1)

        self.assertIsNone(response.errors)
        self.assertUsernameIn(data["payload"])


class VerifyTests(mixins.VerifyMixin, SchemaTestCase):
    query = """
    mutation VerifyToken($token: String!) {
      verifyToken(token: $token) {
        payload
      }
    }"""

    class Mutation(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()


class RefreshTests(mixins.RefreshMixin, SchemaTestCase):
    query = """
    mutation RefreshToken($token: String) {
      refreshToken(token: $token) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = graphql_jwt.Refresh.Field()


class CookieTokenAuthTests(mixins.CookieTokenAuthMixin, CookieTestCase):
    query = """
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()


class CookieRefreshTests(mixins.CookieRefreshMixin, CookieTestCase):
    query = """
    mutation {
      refreshToken {
        token
        payload
        refreshExpiresIn
      }
    }"""

    class Mutation(graphene.ObjectType):
        refresh_token = graphql_jwt.Refresh.Field()


class DeleteCookieTests(mixins.DeleteCookieMixin, CookieTestCase):
    query = """
    mutation {
      deleteCookie {
        deleted
      }
    }"""

    class Mutation(graphene.ObjectType):
        delete_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()
