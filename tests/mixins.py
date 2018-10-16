from datetime import datetime, timedelta

from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token
from graphql_jwt.utils import get_payload

from .compat import mock
from .decorators import override_jwt_settings


class TokenAuthMixin(object):

    def test_token_auth(self):
        response = self.execute({
            'username': self.user.get_username(),
            'password': 'dolphins',
        })

        payload = get_payload(response.data['tokenAuth']['token'])
        self.assertEqual(self.user.get_username(), payload['username'])

    def test_token_auth_invalid_credentials(self):
        response = self.execute({
            'username': self.user.get_username(),
            'password': 'wrong',
        })

        self.assertTrue(response.errors)


class VerifyMixin(object):

    def test_verify(self):
        response = self.execute({
            'token': self.token,
        })

        payload = response.data['verifyToken']['payload']
        self.assertEqual(self.user.get_username(), payload['username'])

    def test_verify_invalid_token(self):
        response = self.execute({
            'token': 'invalid',
        })

        self.assertTrue(response.errors)


class RefreshMixin(object):

    def test_refresh(self):
        with mock.patch('graphql_jwt.utils.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value =\
                datetime.utcnow() + timedelta(seconds=1)

            response = self.execute({
                'token': self.token,
            })

        data = response.data['refreshToken']
        token = data['token']

        self.assertNotEqual(self.token, token)
        self.assertEqual(self.user.get_username(), data['payload']['username'])

        payload = get_payload(token)
        self.assertEqual(self.payload['origIat'], payload['origIat'])

    def test_refresh_expired(self):
        with mock.patch('graphql_jwt.utils.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = datetime.utcnow() +\
                jwt_settings.JWT_REFRESH_EXPIRATION_DELTA +\
                timedelta(seconds=1)

            response = self.execute({
                'token': self.token,
            })

        self.assertTrue(response.errors)

    @override_jwt_settings(JWT_ALLOW_REFRESH=False)
    def test_refresh_error(self):
        token = get_token(self.user)
        response = self.execute({
            'token': token,
        })

        self.assertTrue(response.errors)
