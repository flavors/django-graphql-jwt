import json

from unittest.mock import MagicMock

from django.http import JsonResponse
from graphql_jwt.middleware import JWTMiddleware

from .base import GraphQLJWTTestCase


class MiddlewareTests(GraphQLJWTTestCase):

    def setUp(self):
        super().setUp()

        self.get_response_mock = MagicMock(return_value=JsonResponse({}))
        self.middleware = JWTMiddleware(self.get_response_mock)

    def test_authenticate(self):
        headers = {
            'HTTP_AUTHORIZATION': 'JWT ' + self.token,
        }

        request = self.factory.get('/', **headers)
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)

    def test_graphql_error(self):
        headers = {
            'HTTP_AUTHORIZATION': 'JWT invalid',
        }

        request = self.factory.get('/', **headers)
        response = self.middleware(request)

        self.assertTrue(json.loads(response.content.decode('utf-8'))['errors'])
        self.get_response_mock.assert_not_called()
