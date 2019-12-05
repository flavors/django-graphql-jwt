from graphql_jwt.shortcuts import get_token
from graphql_jwt.utils import get_payload

from .context_managers import back_to_the_future, refresh_expired
from .decorators import override_jwt_settings


class TokenAuthMixin:

    def test_token_auth(self):
        response = self.execute({
            self.user.USERNAME_FIELD: self.user.get_username(),
            'password': 'dolphins',
        })

        payload = get_payload(response.data['tokenAuth']['token'])

        self.assertUsernameIn(payload)

    def test_token_auth_invalid_credentials(self):
        response = self.execute({
            self.user.USERNAME_FIELD: self.user.get_username(),
            'password': 'wrong',
        })

        self.assertIsNotNone(response.errors)


class VerifyMixin:

    def test_verify(self):
        response = self.execute({
            'token': self.token,
        })

        payload = response.data['verifyToken']['payload']

        self.assertUsernameIn(payload)

    def test_verify_invalid_token(self):
        response = self.execute({
            'token': 'invalid',
        })

        self.assertIsNotNone(response.errors)


class RefreshMixin:

    def test_refresh(self):
        with back_to_the_future(seconds=1):
            response = self.execute({
                'token': self.token,
            })

        data = response.data['refreshToken']
        token = data['token']
        payload = get_payload(token)

        self.assertNotEqual(token, self.token)
        self.assertUsernameIn(data['payload'])
        self.assertEqual(payload['origIat'], self.payload['origIat'])
        self.assertGreater(payload['exp'], self.payload['exp'])

    def test_refresh_expired(self):
        with refresh_expired():
            response = self.execute({
                'token': self.token,
            })

        self.assertIsNotNone(response.errors)

    @override_jwt_settings(JWT_ALLOW_REFRESH=False)
    def test_refresh_error(self):
        token = get_token(self.user)
        response = self.execute({
            'token': token,
        })

        self.assertIsNotNone(response.errors)
