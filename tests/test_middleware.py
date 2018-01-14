import json
from unittest.mock import MagicMock, patch

from django.http import JsonResponse

from graphql_jwt import settings as graphql_jwt_settings
from graphql_jwt.middleware import JWTMiddleware

from .testcases import GraphQLJWTTestCase


class MiddlewareTests(GraphQLJWTTestCase):

    def setUp(self):
        super().setUp()

        self.get_response_mock = MagicMock(return_value=JsonResponse({}))
        self.middleware = JWTMiddleware(self.get_response_mock)

    def test_authenticate(self):
        headers = {
            'HTTP_AUTHORIZATION': '{0} {1}'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.factory.get('/', **headers)
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)

    @patch('graphql_jwt.middleware.authenticate', return_value=None)
    def test_user_not_authenticate(self, *args):
        headers = {
            'HTTP_AUTHORIZATION': '{0} {1}'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.factory.get('/', **headers)
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)

    def test_graphql_error(self):
        headers = {
            'HTTP_AUTHORIZATION': '{} invalid'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        request = self.factory.get('/', **headers)
        response = self.middleware(request)
        content = json.loads(response.content.decode('utf-8'))

        self.assertTrue(content['errors'])
        self.get_response_mock.assert_not_called()

    def test_header_not_found(self):
        request = self.factory.get('/')
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)

    def test_user_is_authenticated(self):
        headers = {
            'HTTP_AUTHORIZATION': '{0} {1}'.format(
                graphql_jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.factory.get('/', **headers)
        request.user = self.user
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
