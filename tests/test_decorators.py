from django.contrib.auth import models

from promise import Promise, is_thenable

from graphql_jwt import decorators, exceptions

from .compat import mock
from .testcases import UserTestCase


def info_mock(user):
    return mock.Mock(context=mock.Mock(user=user))


class DecoratorsTests(UserTestCase):

    def test_login_required(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        result = wrapped(info_mock(self.user))
        self.assertIsNone(result)

    def test_login_required_permission_denied(self):

        @decorators.login_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(models.AnonymousUser()))

    def test_staff_member_required(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        self.user.is_staff = True
        result = wrapped(info_mock(self.user))

        self.assertIsNone(result)

    def test_staff_member_required_permission_denied(self):

        @decorators.staff_member_required
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(self.user))

    def test_permission_required(self):

        @decorators.permission_required('auth.add_user')
        def wrapped(info):
            """Decorated function"""

        perm = models.Permission.objects.get(codename='add_user')
        self.user.user_permissions.add(perm)

        result = wrapped(info_mock(self.user))
        self.assertIsNone(result)

    def test_permission_denied(self):

        @decorators.permission_required(['auth.add_user', 'auth.change_user'])
        def wrapped(info):
            """Decorated function"""

        with self.assertRaises(exceptions.PermissionDenied):
            wrapped(info_mock(self.user))

    def test_token_auth_thenable(self):

        @decorators.token_auth
        def wrapped(cls, root, info, **kwargs):
            return Promise()

        result = wrapped(
            self,
            None,
            mock.Mock(),
            password='dolphins',
            username=self.user.get_username())

        self.assertTrue(is_thenable(result))
