from promise import Promise, is_thenable

from graphql_jwt import decorators

from .compat import mock
from .testcases import UserTestCase


class DecoratorsTests(UserTestCase):

    def test_token_auth(self):

        @decorators.token_auth
        def wrapped(self, root, info, **kwargs):
            return Promise()

        root_mock = mock.MagicMock()
        info_mock = mock.MagicMock()

        result = wrapped(
            self,
            root_mock,
            info_mock,
            password='dolphins',
            username=self.user.get_username())

        self.assertTrue(is_thenable(result))
