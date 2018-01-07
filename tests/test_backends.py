from graphql_jwt import settings as graphql_jwt_settings
from graphql_jwt.backends import JWTBackend
from graphql_jwt.exceptions import GraphQLJWTError

from .base import GraphQLJWTTestCase


class BackendsTests(GraphQLJWTTestCase):

    def test_authenticate(self):
        headers = {
            'HTTP_AUTHORIZATION': '{0} {1}'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.factory.get('/', **headers)
        user = JWTBackend().authenticate(request=request)

        self.assertEqual(user, self.user)

    def test_authenticate_fail(self):
        headers = {
            'HTTP_AUTHORIZATION': '{} invalid'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        request = self.factory.get('/', **headers)

        with self.assertRaises(GraphQLJWTError):
            JWTBackend().authenticate(request=request)

    def test_authenticate_null_request(self):
        user = JWTBackend().authenticate(request=None)
        self.assertIsNone(user)

    def test_authenticate_missing_token(self):
        request = self.factory.get('/')
        user = JWTBackend().authenticate(request=request)

        self.assertIsNone(user)

    def test_get_user(self):
        user = JWTBackend().get_user(self.user.username)
        self.assertEqual(user, self.user)
