from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token
from graphql_jwt.signals import token_issued, token_refreshed

from .context_managers import back_to_the_future, catch_signal, refresh_expired
from .decorators import override_jwt_settings


class TokenAuthMixin:
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

    def test_token_auth_invalid_credentials(self):
        response = self.execute(
            {
                self.user.USERNAME_FIELD: self.user.get_username(),
                "password": "wrong",
            }
        )

        self.assertIsNotNone(response.errors)


class VerifyMixin:
    def test_verify(self):
        response = self.execute(
            {
                "token": self.token,
            }
        )

        payload = response.data["verifyToken"]["payload"]

        self.assertIsNone(response.errors)
        self.assertUsernameIn(payload)

    def test_verify_invalid_token(self):
        response = self.execute(
            {
                "token": "invalid",
            }
        )

        self.assertIsNotNone(response.errors)


class RefreshMixin:
    def test_refresh(self):
        with catch_signal(
            token_refreshed
        ) as token_refreshed_handler, back_to_the_future(seconds=1):
            response = self.execute(
                {
                    "token": self.token,
                }
            )

        data = response.data["refreshToken"]
        token = data["token"]
        payload = data["payload"]

        self.assertEqual(token_refreshed_handler.call_count, 1)

        self.assertIsNone(response.errors)
        self.assertNotEqual(token, self.token)
        self.assertUsernameIn(data["payload"])
        self.assertEqual(payload["origIat"], self.payload["origIat"])
        self.assertGreater(payload["exp"], self.payload["exp"])

    def test_missing_token(self):
        response = self.execute({})
        self.assertIsNotNone(response.errors)

    def test_refresh_expired(self):
        with refresh_expired():
            response = self.execute(
                {
                    "token": self.token,
                }
            )

        self.assertIsNotNone(response.errors)

    @override_jwt_settings(JWT_ALLOW_REFRESH=False)
    def test_refresh_error(self):
        token = get_token(self.user)
        response = self.execute(
            {
                "token": token,
            }
        )

        self.assertIsNotNone(response.errors)


class CookieTokenAuthMixin:
    def test_token_auth(self):
        response = self.execute(
            {
                self.user.USERNAME_FIELD: self.user.get_username(),
                "password": "dolphins",
            }
        )

        data = response.data["tokenAuth"]
        token = response.cookies.get(jwt_settings.JWT_COOKIE_NAME).value

        self.assertIsNone(response.errors)
        self.assertEqual(token, data["token"])
        self.assertUsernameIn(data["payload"])


class CookieRefreshMixin:
    def test_refresh(self):
        self.set_cookie()

        with back_to_the_future(seconds=1):
            response = self.execute()

        data = response.data["refreshToken"]
        token = data["token"]

        self.assertIsNone(response.errors)
        self.assertNotEqual(token, self.token)
        self.assertUsernameIn(data["payload"])


class DeleteCookieMixin:
    def test_delete_cookie(self):
        self.set_cookie()

        response = self.execute()
        data = response.data["deleteCookie"]

        self.assertIsNone(response.errors)
        self.assertTrue(data["deleted"])
