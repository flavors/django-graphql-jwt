import graphene

import graphql_jwt
from graphql_jwt.utils import get_payload

from .testcases import CookieGraphQLViewTestCase


class TokenAuthTests(CookieGraphQLViewTestCase):
    query = '''
    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
      }
    }'''

    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    def test_token_auth(self):
        response = self.execute({
            self.user.USERNAME_FIELD: self.user.get_username(),
            'password': 'dolphins',
        })

        token = response.cookies.get('JWT').value
        payload = get_payload(token)

        self.assertEqual(token, response.data['tokenAuth']['token'])
        self.assertUsernameIn(payload)


class ViewerTests(CookieGraphQLViewTestCase):
    query = '''
    {
      viewer
    }'''

    class Query(graphene.ObjectType):
        viewer = graphene.String()

        def resolve_viewer(self, info):
            return info.context.user.username

    def test_viewer(self):
        self.authenticate()
        response = self.execute()

        self.assertEqual(self.user.get_username(), response.data['viewer'])
