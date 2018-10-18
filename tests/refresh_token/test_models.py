from graphql_jwt.shortcuts import create_refresh_token

from ..testcases import UserTestCase


class ModelsTests(UserTestCase):

    def setUp(self):
        super(ModelsTests, self).setUp()
        self.refresh_token = create_refresh_token(self.user)

    def test_str(self):
        self.assertEqual(str(self.refresh_token), self.refresh_token.token)
