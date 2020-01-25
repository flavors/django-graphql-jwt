from django.contrib.admin import site

from graphql_jwt.refresh_token import admin
from graphql_jwt.refresh_token.utils import get_refresh_token_model
from graphql_jwt.shortcuts import create_refresh_token

from ..decorators import skipif_django_version
from ..testcases import TestCase


class AdminTestCase(TestCase):

    def setUp(self):
        super().setUp()
        RefreshToken = get_refresh_token_model()
        self.refresh_token = create_refresh_token(self.user)
        self.refresh_token_admin = admin.RefreshTokenAdmin(RefreshToken, site)


class AdminTests(AdminTestCase):

    def test_revoke(self):
        request = self.request_factory.get('/')
        qs = self.refresh_token_admin.get_queryset(request)

        self.refresh_token_admin.revoke(request, qs)
        self.refresh_token.refresh_from_db()

        self.assertIsNotNone(self.refresh_token.revoked)

    def test_is_expired(self):
        is_expired = self.refresh_token_admin.is_expired(self.refresh_token)

        self.assertFalse(is_expired)


class FiltersTests(AdminTestCase):

    def filter_queryset(self, **kwargs):
        request = self.request_factory.get('/', kwargs)
        request.user = self.user
        changelist = self.refresh_token_admin.get_changelist_instance(request)
        return changelist.get_queryset(request)

    @skipif_django_version('2.0')
    def test_revoked(self):
        qs = self.filter_queryset(revoked='yes')
        self.assertFalse(qs)

    @skipif_django_version('2.0')
    def test_not_revoked(self):
        qs = self.filter_queryset(revoked='no')
        self.assertTrue(qs)

    @skipif_django_version('2.0')
    def test_expired(self):
        qs = self.filter_queryset(expired='yes')
        self.assertFalse(qs)

    @skipif_django_version('2.0')
    def test_not_expired(self):
        qs = self.filter_queryset(expired='no')
        self.assertTrue(qs)
