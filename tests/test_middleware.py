from unittest import mock

from django.contrib.auth.models import AnonymousUser

import graphene
from graphql import OperationDefinitionNode, OperationType

import graphql_jwt
from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.middleware import JSONWebTokenMiddleware, allow_any
from graphql_jwt.settings import jwt_settings

from .decorators import override_jwt_settings
from .testcases import ResolveInfoTestCase


class AuthenticateByHeaderTests(ResolveInfoTestCase):
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
        info_mock = self.info_mock(user=AnonymousUser(), headers=headers)

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
        info_mock = self.info_mock(user=AnonymousUser(), headers=headers)

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
        info_mock = self.info_mock(user=AnonymousUser(), headers=headers)

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
        info_mock = self.info_mock(user=self.user, headers=headers)

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
        info_mock = self.info_mock(user=AnonymousUser(), headers=headers)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    def test_authenticate_context(self):
        info_mock = self.info_mock(path=["path"])

        self.middleware.cached_allow_any.add("path")
        authenticate_context = self.middleware.authenticate_context(info_mock)

        self.assertFalse(authenticate_context)


class AuthenticateByArgumentTests(ResolveInfoTestCase):
    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def setUp(self):
        super().setUp()
        self.middleware = JSONWebTokenMiddleware()

    @override_jwt_settings(
        JWT_ALLOW_ARGUMENT=True,
        JWT_ALLOW_ANY_HANDLER=lambda *args, **kwargs: False,
    )
    def test_authenticate(self):
        kwargs = {
            jwt_settings.JWT_ARGUMENT_NAME: self.token,
        }

        next_mock = mock.Mock()
        info_mock = self.info_mock(AnonymousUser())

        self.middleware.resolve(next_mock, None, info_mock, **kwargs)

        next_mock.assert_called_once_with(None, info_mock, **kwargs)
        self.assertEqual(info_mock.context.user, self.user)

        user = self.middleware.cached_authentication[tuple(info_mock.path)]
        self.assertEqual(user, self.user)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_authenticate_parent(self):
        next_mock = mock.Mock()
        info_mock = self.info_mock(user=AnonymousUser(), path=["0", "1"])

        self.middleware.cached_authentication.insert(["0"], self.user)
        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertEqual(info_mock.context.user, self.user)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_clear_authentication(self):
        next_mock = mock.Mock()
        info_mock = self.info_mock(self.user)

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_clear_session_authentication(self):
        next_mock = mock.Mock()
        info_mock = self.info_mock(self.user)
        info_mock.context.session = self.client.session

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertIsInstance(info_mock.context.user, AnonymousUser)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_context_has_not_attr_user(self):
        next_mock = mock.Mock()
        info_mock = self.info_mock()

        self.middleware.resolve(next_mock, None, info_mock)

        next_mock.assert_called_once_with(None, info_mock)
        self.assertFalse(hasattr(info_mock.context, "user"))


class AllowAnyMutation(graphene.Mutation):
    def mutate(root, info):
        return None


class AllowAnyTests(ResolveInfoTestCase):
    def info_mock(self, user, **kwargs):
        class Mutation(graphene.ObjectType):
            test = AllowAnyMutation.Field()
            verify = graphql_jwt.Verify.Field()

        schema = graphene.Schema(mutation=Mutation).graphql_schema
        operation = OperationDefinitionNode(operation=OperationType("mutation"))

        return super().info_mock(
            user=user,
            schema=schema,
            operation=operation,
            **kwargs,
        )

    @override_jwt_settings(JWT_ALLOW_ANY_CLASSES=[f"{__name__}.AllowAnyMutation"])
    def test_allow_any(self):
        info_mock = self.info_mock(self.user, field_name="test")
        allowed = allow_any(info_mock)

        self.assertTrue(allowed)

    def test_allow_jwt_mutations(self):
        info_mock = self.info_mock(user=self.user, field_name="verify")
        allowed = allow_any(info_mock)

        self.assertTrue(allowed)

    def test_unknown_field(self):
        info_mock = self.info_mock(self.user)
        allowed = allow_any(info_mock)

        self.assertFalse(allowed)

    def test_not_allow_any(self):
        info_mock = self.info_mock(self.user, field_name="test")
        allowed = allow_any(info_mock)

        self.assertFalse(allowed)
