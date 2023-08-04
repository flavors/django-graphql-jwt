import django
from django.contrib.auth.models import AnonymousUser, Permission

from graphql_jwt import decorators, exceptions

from .decorators import override_jwt_settings
from .testcases import ResolveInfoTestCase


class UserPassesTests(ResolveInfoTestCase):
    def test_user_passes_test(self):
        result = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk,
        )(
            lambda info: None
        )(self.info_mock(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.user_passes_test(
            lambda u: u.pk == self.user.pk + 1,
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info_mock(self.user))


class LoginRequiredTests(ResolveInfoTestCase):
    def test_login_required(self):
        result = decorators.login_required(
            lambda info: None,
        )(self.info_mock(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.login_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info_mock(AnonymousUser()))


class StaffMemberRequiredTests(ResolveInfoTestCase):
    def test_staff_member_required(self):
        self.user.is_staff = True

        result = decorators.staff_member_required(
            lambda info: None,
        )(self.info_mock(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.staff_member_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info_mock(self.user))


class SuperuserRequiredTests(ResolveInfoTestCase):
    def test_superuser_required(self):
        self.user.is_superuser = True

        result = decorators.superuser_required(
            lambda info: None,
        )(self.info_mock(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.superuser_required(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info_mock(self.user))


class PermissionRequiredTests(ResolveInfoTestCase):
    def test_permission_required(self):
        perm = Permission.objects.get(codename="add_user")
        self.user.user_permissions.add(perm)

        result = decorators.permission_required("auth.add_user")(
            lambda info: None,
        )(self.info_mock(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):
        func = decorators.permission_required(
            ["auth.add_user", "auth.change_user"],
        )(lambda info: None)

        with self.assertRaises(exceptions.PermissionDenied):
            func(self.info_mock(self.user))


class CSRFRotationTests(ResolveInfoTestCase):
    @override_jwt_settings(JWT_CSRF_ROTATION=True)
    def test_csrf_rotation(self):
        info_mock = self.info_mock(AnonymousUser())
        decorators.csrf_rotation(
            lambda cls, root, info, *args, **kwargs: None,
        )(self, None, info_mock)

        if django.VERSION >= (4,):
            self.assertTrue(info_mock.context.META["CSRF_COOKIE_NEEDS_UPDATE"])
        else:
            self.assertTrue(info_mock.context.csrf_cookie_needs_reset)
