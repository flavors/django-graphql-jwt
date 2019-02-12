from django.contrib.auth.models import AnonymousUser, Permission

from promise import Promise, is_thenable

from graphql_jwt import decorators, exceptions

from .testcases import TestCase


class UserPassesTests(TestCase):

    def test_user_passes_test(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk)
        def wrapped(info):
            """Decorated function"""

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.user_passes_test(lambda u: u.pk == self.user.pk + 1)
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class LoginRequiredTests(TestCase):

    def test_login_required(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(AnonymousUser()))


class StaffMemberRequiredTests(TestCase):

    def test_staff_member_required(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        self.user.is_staff = True
        result = wrapped(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class SuperuserRequiredTests(TestCase):

    def test_superuser_required(self):

        @decorators.superuser_required
        def wrapped(info):
            """Decorated function"""

        self.user.is_superuser = True
        result = wrapped(self.info(self.user))

        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.superuser_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class PermissionRequiredTests(TestCase):

    def test_permission_required(self):

        @decorators.permission_required('auth.add_user')
        def wrapped(info):
            """Decorated function"""

        perm = Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = wrapped(self.info(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.permission_required(['auth.add_user', 'auth.change_user'])
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(self.info(self.user))


class TokenAuthTests(TestCase):

    def test_is_thenable(self):

        @decorators.token_auth
        def wrapped(cls, root, info, **kwargs):
            return Promise()

        info_mock = self.info(AnonymousUser())

        result = wrapped(
            self,
            None,
            info_mock,
            password='dolphins',
            username=self.user.get_username())

        self.assertTrue(is_thenable(result))
