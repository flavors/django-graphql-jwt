from unittest import mock

from django.contrib.auth.models import AnonymousUser, Permission

from promise import Promise, is_thenable

from graphql_jwt import decorators, exceptions

from .decorators import override_jwt_settings
from .testcases import TestCase


class UserPassesTests(TestCase):

    def test_user_passes_test(self):
        result = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk,
        )(lambda info: None)(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk + 1,
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class LoginRequiredTests(TestCase):

    def test_login_required(self):
        result = decorators.login_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.login_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(AnonymousUser()))


class StaffMemberRequiredTests(TestCase):

    def test_staff_member_required(self):
        self.user.is_staff = True

        result = decorators.staff_member_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.staff_member_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class SuperuserRequiredTests(TestCase):

    def test_superuser_required(self):
        self.user.is_superuser = True

        result = decorators.superuser_required(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.superuser_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class PermissionRequiredTests(TestCase):

    def test_permission_required(self):
        perm = Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = decorators.permission_required('auth.add_user')(
            lambda info: None,
        )(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.permission_required(
            ['auth.add_user', 'auth.change_user'],
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info(self.user))


class TokenAuthTests(TestCase):

    def test_is_thenable(self):
        info_mock = self.info(AnonymousUser())
        func = decorators.token_auth(
            lambda cls, root, info, **kwargs: Promise(),
        )
        result = func(
            self,
            None,
            info_mock,
            password='dolphins',
            username=self.user.get_username(),
        )

        self.assertTrue(is_thenable(result))

    @override_jwt_settings(JWT_CSRF_ROTATION=True)
    def test_csrf_rotation(self):
        info_mock = self.info(AnonymousUser())
        func = decorators.token_auth(
            lambda cls, root, info, **kwargs: mock.Mock(),
        )
        func(
            self,
            None,
            info_mock,
            password='dolphins',
            username=self.user.get_username(),
        )

        self.assertTrue(info_mock.context.csrf_cookie_needs_reset)
