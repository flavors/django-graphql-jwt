from unittest import mock

from django.contrib.auth.models import AnonymousUser

from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.middleware import JSONWebTokenMiddleware, allow_any
from graphql_jwt.settings import jwt_settings

from .decorators import override_jwt_settings
from .testcases import TestCase


class AuthenticateByHeaderTests(TestCase):
    def setUp(self):
        super().setUp()
        self.middleware = JSONWebTokenMiddleware()

    @override_jwt_settings(JWT_ALLOW_ANY_HANDLER=lambda *args: False)
    def test_authenticate(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {self.token}"
            ),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertEqual(info_mock.context.user, self.user)

    @override_jwt_settings(JWT_ALLOW_ANY_HANDLER=lambda *args: False)
    @mock.patch("graphql_jwt.middleware.authenticate", return_value=None)
    def test_not_authenticate(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {self.token}"
            ),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        authenticate_mock.assert_called_once_with(request=info_mock.context)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @override_jwt_settings(JWT_ALLOW_ANY_HANDLER=lambda *args: False)
    def test_invalid_token(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} invalid"
            ),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        with self.assertRaises(JSONWebTokenError):
            self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_not_called()

    @mock.patch("graphql_jwt.middleware.authenticate")
    def test_already_authenticated(self, authenticate_mock):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {self.token}"
            ),
        }

        next_mock = mock.Mock()
        info_mock = self.info(self.user, **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        authenticate_mock.assert_not_called()

    @override_jwt_settings(JWT_ALLOW_ANY_HANDLER=lambda *args: True)
    def test_allow_any(self):
        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: (
                f"{jwt_settings.JWT_AUTH_HEADER_PREFIX} {self.token}"
            ),
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser(), **headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    def test_authenticate_context(self):
        info_mock = self.info()

        self.middleware.cached_allow_any.add("test")
        authenticate_context = self.middleware.authenticate_context(info_mock)

        self.assertFalse(authenticate_context)


class AuthenticateByArgumentTests(TestCase):
    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def setUp(self):
        super().setUp()
        self.middleware = JSONWebTokenMiddleware()

    @override_jwt_settings(
        JWT_ALLOW_ARGUMENT=True, JWT_ALLOW_ANY_HANDLER=lambda *args, **kwargs: False
    )
    def test_authenticate(self):
        kwargs = {
            jwt_settings.JWT_ARGUMENT_NAME: self.token,
        }

        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser())

        self.middleware.resolve(next_mock, None, info_mock, **kwargs)

        next_mock.assert_called_once_with(None, info_mock, **kwargs)
        self.assertEqual(info_mock.context.user, self.user)

        user = self.middleware.cached_authentication[tuple(info_mock.path)]
        self.assertEqual(user, self.user)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_authenticate_parent(self):
        next_mock = mock.Mock()
        info_mock = self.info(AnonymousUser())
        info_mock.path = ["0", "1"]

        self.middleware.cached_authentication.insert(["0"], self.user)
        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertEqual(info_mock.context.user, self.user)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_clear_authentication(self):
        next_mock = mock.Mock()
        info_mock = self.info(self.user)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_clear_session_authentication(self):
        next_mock = mock.Mock()
        info_mock = self.info(self.user)
        info_mock.context.session = self.client.session

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_context_has_not_attr_user(self):
        next_mock = mock.Mock()
        info_mock = self.info()

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertFalse(hasattr(info_mock.context, "user"))


class AllowAnyTests(TestCase):
    def info(self, user, **headers):
        info_mock = super().info(user, **headers)
        info_mock.field_name = "test"
        info_mock.operation.operation.value = "query"
        return info_mock

    def info_with_field_mock(self, user, field=None):
        info_mock = self.info(user)
        info_mock.schema.query_type = mock.Mock(
            fields={
                "test": field,
            }
        )
        return info_mock

    def info_with_type_mock(self, user, type=None):
        type_mock = mock.Mock(type=mock.Mock(graphene_type=type))
        return self.info_with_field_mock(user, type_mock)

    @override_jwt_settings(JWT_ALLOW_ANY_CLASSES=["tests.testcases.TestCase"])
    def test_allow_any(self):
        info_mock = self.info_with_type_mock(self.user, TestCase)
        allowed = allow_any(info_mock)

        self.assertTrue(allowed)

    def test_not_allow_any(self):
        info_mock = self.info_with_type_mock(self.user, TestCase)
        allowed = allow_any(info_mock)

        self.assertFalse(allowed)

    def test_unknown_field(self):
        info_mock = self.info_with_field_mock(self.user)
        allowed = allow_any(info_mock)

        self.assertFalse(allowed)

    def test_unknown_type(self):
        info_mock = self.info_with_type_mock(self.user)
        allowed = allow_any(info_mock)

        self.assertFalse(allowed)
