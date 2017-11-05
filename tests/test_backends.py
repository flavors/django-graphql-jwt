from graphql_jwt.backends import JWTBackend
from graphql_jwt.exceptions import GraphQLJWTError

from .base import GraphQLJWTTestCase


class BackendsTests(GraphQLJWTTestCase):

    def test_authenticate(self):
        headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + self.token,
        }

        request = self.factory.get('/', **headers)
        user = JWTBackend().authenticate(request=request)

        self.assertEqual(user, self.user)

    def test_authenticate_fail(self):
        headers = {
            'HTTP_AUTHORIZATION': 'JWT invalid',
        }

        request = self.factory.get('/', **headers)

        with self.assertRaises(GraphQLJWTError):
            JWTBackend().authenticate(request=request)

    def test_get_user(self):
        user = JWTBackend().get_user(self.user.username)
        self.assertEqual(user, self.user)
