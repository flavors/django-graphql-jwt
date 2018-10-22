from datetime import timedelta

from graphql_jwt import exceptions, utils
from graphql_jwt.settings import jwt_settings

from .compat import mock
from .decorators import override_jwt_settings
from .testcases import TestCase


class UtilsTests(TestCase):

    @mock.patch('django.contrib.auth.models.User.get_username',
                return_value=mock.Mock(pk='test'))
    def test_payload_foreign_key_pk(self, *args):
        payload = utils.jwt_payload(self.user)
        username = jwt_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER(payload)

        self.assertEqual(username, 'test')

    @override_jwt_settings(JWT_AUDIENCE='test')
    def test_payload_audience(self):
        payload = utils.jwt_payload(self.user)
        self.assertEqual(payload['aud'], 'test')

    @override_jwt_settings(JWT_ISSUER='test')
    def test_payload_issuer(self):
        payload = utils.jwt_payload(self.user)
        self.assertEqual(payload['iss'], 'test')

    def test_invalid_authorization_header_prefix(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: 'INVALID token',
        }

        request = self.request_factory.get('/', **headers)
        authorization_header = utils.get_authorization_header(request)

        self.assertIsNone(authorization_header)

    @override_jwt_settings(JWT_AUTH_HEADER='HTTP_AUTHORIZATION_TOKEN')
    def test_custom_authorization_header(self):
        headers = {
            'HTTP_AUTHORIZATION_TOKEN': '{} token'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        request = self.request_factory.get('/', **headers)
        authorization_header = utils.get_authorization_header(request)

        self.assertEqual(authorization_header, 'token')

    @override_jwt_settings(
        JWT_VERIFY_EXPIRATION=True,
        JWT_EXPIRATION_DELTA=timedelta(seconds=-1))
    def test_payload_expired_signature(self):
        payload = utils.jwt_payload(self.user)
        token = utils.jwt_encode(payload)

        with self.assertRaises(exceptions.JSONWebTokenExpired):
            utils.get_payload(token)

    def test_payload_decode_audience_missing(self):
        payload = utils.jwt_payload(self.user)
        token = utils.jwt_encode(payload)

        with override_jwt_settings(JWT_AUDIENCE='test'):
            with self.assertRaises(exceptions.JSONWebTokenError):
                utils.get_payload(token)

    def test_payload_decode_error(self):
        with self.assertRaises(exceptions.JSONWebTokenError):
            utils.get_payload('invalid')

    def test_user_by_natural_key_not_exists(self):
        user = utils.get_user_by_natural_key(0)
        self.assertIsNone(user)

    def test_user_by_invalid_payload(self):
        with self.assertRaises(exceptions.JSONWebTokenError):
            utils.get_user_by_payload({})

    @mock.patch('django.contrib.auth.models.User.is_active',
                new_callable=mock.PropertyMock,
                return_value=False)
    def test_user_disabled_by_payload(self, *args):
        payload = utils.jwt_payload(self.user)

        with self.assertRaises(exceptions.JSONWebTokenError):
            utils.get_user_by_payload(payload)
