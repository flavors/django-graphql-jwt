from graphql_jwt.backends import JSONWebTokenBackend
from graphql_jwt.exceptions import GraphQLJWTError
from graphql_jwt.settings import jwt_settings

from .testcases import GraphQLJWTTestCase


class BackendsTests(GraphQLJWTTestCase):

    def test_authenticate(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.factory.get('/', **headers)
        user = JSONWebTokenBackend().authenticate(request=request)

        self.assertEqual(user, self.user)

    def test_authenticate_fail(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{} invalid'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        request = self.factory.get('/', **headers)

        with self.assertRaises(GraphQLJWTError):
            JSONWebTokenBackend().authenticate(request=request)

    def test_authenticate_null_request(self):
        user = JSONWebTokenBackend().authenticate(request=None)
        self.assertIsNone(user)

    def test_authenticate_missing_token(self):
        request = self.factory.get('/')
        user = JSONWebTokenBackend().authenticate(request=request)

        self.assertIsNone(user)

    def test_get_user(self):
        user = JSONWebTokenBackend().get_user(self.user.get_username())
        self.assertEqual(user, self.user)
