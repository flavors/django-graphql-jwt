from graphql_jwt.refresh_token.models import AbstractRefreshToken
from graphql_jwt.refresh_token.signals import refresh_token_revoked
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import create_refresh_token

from ..context_managers import catch_signal, refresh_expired
from ..testcases import UserTestCase


class AbstractRefreshTokenTests(UserTestCase):

    def setUp(self):
        super().setUp()
        self.refresh_token = create_refresh_token(self.user)

    def test_str(self):
        self.assertEqual(str(self.refresh_token), self.refresh_token.token)

    def test_generate_token(self):
        token = self.refresh_token.generate_token()
        n_bytes = jwt_settings.JWT_REFRESH_TOKEN_N_BYTES

        self.assertEqual(len(token), n_bytes * 2)

    def test_get_token(self):
        self.refresh_token.token = 'hashed'
        token = self.refresh_token.get_token()

        self.assertEqual(self.refresh_token._cached_token, token)
        self.assertNotEqual(self.refresh_token.token, token)

        del self.refresh_token._cached_token
        token = self.refresh_token.get_token()

        self.assertEqual(self.refresh_token.token, token)

    def test_is_expired(self):
        with refresh_expired():
            self.assertTrue(self.refresh_token.is_expired())

    def test_revoke(self):
        with catch_signal(refresh_token_revoked) as \
                refresh_token_revoked_handler:

            self.refresh_token.revoke()

        self.assertIsNotNone(self.refresh_token.revoked)

        refresh_token_revoked_handler.assert_called_once_with(
            sender=AbstractRefreshToken,
            signal=refresh_token_revoked,
            request=None,
            refresh_token=self.refresh_token,
        )

    def test_reuse(self):
        token = self.refresh_token.token
        created = self.refresh_token.created

        self.refresh_token.reuse()

        self.assertNotEqual(self.refresh_token.token, token)
        self.assertGreater(self.refresh_token.created, created)
