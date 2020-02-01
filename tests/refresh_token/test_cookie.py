import graphql_jwt
from graphql_jwt.refresh_token import signals
from graphql_jwt.settings import jwt_settings

from ..context_managers import back_to_the_future, catch_signal
from ..decorators import override_jwt_settings
from ..testcases import CookieTestCase
from .mixins import RefreshTokenMutationMixin
from .mutations import Refresh
from .testcases import RefreshTokenCookieTestCase


class TokenAuthTests(RefreshTokenMutationMixin, CookieTestCase):
    query = '''
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        payload
        refreshToken
        refreshExpiresIn
      }
    }'''

    refresh_token_mutations = {
        'token_auth': graphql_jwt.ObtainJSONWebToken,
    }

    @override_jwt_settings(JWT_LONG_RUNNING_REFRESH_TOKEN=True)
    def test_token_auth(self):
        response = self.execute({
            self.user.USERNAME_FIELD: self.user.get_username(),
            'password': 'dolphins',
        })

        data = response.data['tokenAuth']
        token = response.cookies.get(
            jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
        ).value

        self.assertIsNone(response.errors)
        self.assertEqual(token, response.data['tokenAuth']['refreshToken'])
        self.assertUsernameIn(data['payload'])


class RefreshTokenTests(RefreshTokenMutationMixin, RefreshTokenCookieTestCase):
    query = '''
    mutation {
      refreshToken {
        token
        payload
        refreshToken
        refreshExpiresIn
      }
    }'''

    refresh_token_mutations = {
        'refresh_token': Refresh,
    }

    def test_refresh_token(self):
        self.set_refresh_token_cookie()

        with catch_signal(signals.refresh_token_rotated) as \
                refresh_token_rotated_handler, back_to_the_future(seconds=1):

            response = self.execute()

        data = response.data['refreshToken']
        token = data['token']

        self.assertIsNone(response.errors)
        self.assertEqual(refresh_token_rotated_handler.call_count, 1)

        self.assertNotEqual(token, self.token)
        self.assertUsernameIn(data['payload'])
