from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import create_refresh_token

from ..testcases import CookieClient, CookieTestCase


class RefreshTokenCookieClient(CookieClient):

    def set_refresh_token_cookie(self, token):
        self.cookies[jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME] = token


class RefreshTokenCookieTestCase(CookieTestCase):
    client_class = RefreshTokenCookieClient

    def setUp(self):
        super().setUp()
        self.refresh_token = create_refresh_token(self.user)

    def set_refresh_token_cookie(self):
        self.client.set_refresh_token_cookie(self.refresh_token.token)
