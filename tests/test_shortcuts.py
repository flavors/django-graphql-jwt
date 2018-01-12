from django.contrib.auth import get_user_model
from django.test import TestCase

from graphql_jwt import shortcuts


class ShortcutsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test')

    def test_get_token(self):
        token = shortcuts.get_token(self.user)
        user = shortcuts.get_user_by_token(token)

        self.assertEqual(user, self.user)
