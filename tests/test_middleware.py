import json
import warnings

from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse

from graphene_django.settings import graphene_settings

from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.middleware import JSONWebTokenMiddleware, is_authenticated
from graphql_jwt.mutations import JSONWebTokenMutation
from graphql_jwt.settings import jwt_settings

from .compat import mock
from .decorators import override_jwt_settings
from .testcases import TestCase


class DjangoMiddlewareTests(TestCase):

    def setUp(self):
        super(DjangoMiddlewareTests, self).setUp()

        self.get_response_mock = mock.Mock(return_value=JsonResponse({}))
        self.middleware = JSONWebTokenMiddleware(self.get_response_mock)

    def test_authenticate(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.request_factory.get('/', **headers)
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
        self.assertEqual(request.user, self.user)

    @mock.patch('graphql_jwt.middleware.authenticate', return_value=None)
    def test_not_authenticate(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.request_factory.get('/', **headers)
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
        authenticate_mock.assert_called_with(request=request)
        self.assertFalse(hasattr(request, 'user'))

    def test_invalid_token(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{} invalid'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        request = self.request_factory.get('/', **headers)
        response = self.middleware(request)
        content = json.loads(response.content.decode('utf-8'))

        self.assertIsNotNone(content['errors'])
        self.get_response_mock.assert_not_called()

    def test_header_not_found(self):
        request = self.request_factory.get('/')
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
        self.assertFalse(hasattr(request, 'user'))

    @mock.patch('graphql_jwt.middleware.authenticate')
    def test_already_authenticated(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        request = self.request_factory.get('/', **headers)
        request.user = self.user
        self.middleware(request)

        self.get_response_mock.assert_called_once_with(request)
        authenticate_mock.assert_not_called()


def is_authenticated_settings(is_authenticated):
    return override_jwt_settings(
        JWT_IS_AUTHENTICATED_HANDLER=lambda info, field: is_authenticated,
    )


class GrapheneMiddlewareTests(TestCase):

    def setUp(self):
        super(GrapheneMiddlewareTests, self).setUp()
        self.middleware = JSONWebTokenMiddleware()

    def info(self, user, **headers):
        info_mock = super(GrapheneMiddlewareTests, self).info(user, **headers)
        info_mock.path = ['test']
        type(info_mock.operation).operation = 'query'
        return info_mock

    def test_deprecation_warning(self):
        graphene_settings.MIDDLEWARE = []

        with warnings.catch_warnings(record=True) as warning_list:
            JSONWebTokenMiddleware()
            self.assertTrue(warning_list)

        graphene_settings.MIDDLEWARE = [JSONWebTokenMiddleware]

    @is_authenticated_settings(True)
    def test_authenticate(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_with(None, info_mock)
        info_mock.schema.get_query_type().fields.get.assert_called_with('test')
        self.assertEqual(info_mock.context.user, self.user)

    @is_authenticated_settings(True)
    @mock.patch('graphql_jwt.middleware.authenticate', return_value=None)
    def test_not_authenticate(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_with(None, info_mock)
        info_mock.schema.get_query_type().fields.get.assert_called_with('test')
        authenticate_mock.assert_called_with(request=info_mock.context)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @is_authenticated_settings(True)
    def test_invalid_token(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{} invalid'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        with self.assertRaises(JSONWebTokenError):
            self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_not_called()
        info_mock.schema.get_query_type().fields.get.assert_called_with('test')

    @is_authenticated_settings(True)
    @mock.patch('graphql_jwt.middleware.authenticate')
    def test_already_authenticated(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        next_mock = mock.Mock()
        info_mock = self.info(self.user, **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_with(None, info_mock)
        info_mock.assert_not_called()
        authenticate_mock.assert_not_called()

    @is_authenticated_settings(False)
    def test_is_not_authenticated(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_with(None, info_mock)
        info_mock.assert_not_called()
        self.assertIsInstance(info_mock.context.user, AnonymousUser)


class IsAuthenticatedTests(TestCase):

    def field(self, cls):
        return mock.Mock(type=mock.Mock(graphene_type=cls))

    def test_not_authenticated(self):
        authenticated = is_authenticated(
            self.info(self.user),
            self.field(JSONWebTokenMutation))

        self.assertFalse(authenticated)

    def test_authenticated(self):
        authenticated = is_authenticated(
            self.info(self.user),
            self.field(TestCase))

        self.assertTrue(authenticated)
