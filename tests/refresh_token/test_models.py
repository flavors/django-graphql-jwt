from graphql_jwt.refresh_token import signals
from graphql_jwt.refresh_token.models import AbstractRefreshToken
from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import create_refresh_token

from ..context_managers import catch_signal, refresh_expired
from ..testcases import UserTestCase


class AbstractRefreshTokenTests(UserTestCase):

    def setUp(self):
        super(AbstractRefreshTokenTests, self).setUp()
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
        with catch_signal(signals.refresh_token_revoked) as handler:
            self.refresh_token.revoke()

        self.assertIsNotNone(self.refresh_token.revoked)

        handler.assert_called_once_with(
            sender=AbstractRefreshToken,
            signal=signals.refresh_token_revoked,
            request=None,
            refresh_token=self.refresh_token,
        )

    def test_rotate(self):
        with catch_signal(signals.refresh_token_rotated) as handler:
            self.refresh_token.rotate()

        handler.assert_called_once_with(
            sender=AbstractRefreshToken,
            signal=signals.refresh_token_rotated,
            request=None,
            refresh_token=self.refresh_token,
        )
