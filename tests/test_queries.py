from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser

import graphene
from graphene.types.generic import GenericScalar

from graphql_jwt.settings import jwt_settings
from graphql_jwt.shortcuts import get_token

from .decorators import override_jwt_settings
from .testcases import SchemaTestCase


class QueriesTests(SchemaTestCase):

    class Query(graphene.ObjectType):
        test = GenericScalar(**{
            jwt_settings.JWT_ARGUMENT_NAME: graphene.String(),
        })

        def resolve_test(self, info, **kwargs):
            return info.context.user

    def setUp(self):
        super(QueriesTests, self).setUp()

        self.other_user = get_user_model().objects.create_user('other')
        self.other_token = get_token(self.other_user)

    @override_jwt_settings(JWT_ALLOW_ARGUMENT=True)
    def test_multiple_credentials(self):
        query = '''
        query Tests($token: String!, $otherToken: String!) {{
          testBegin: test
          testToken: test({0}: $token)
          testOtherToken: test({0}: $otherToken)
          testInvalidToken: test({0}: "invalid")
          testEnd: test
        }}'''.format(jwt_settings.JWT_ARGUMENT_NAME)

        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                self.token,
            ),
        }

        variables = {
            'token': self.token,
            'otherToken': self.other_token,
        }

        response = self.client.execute(query, variables, **headers)
        data = response.data

        self.assertEqual(data['testBegin'], self.user)
        self.assertEqual(data['testEnd'], self.user)
        self.assertEqual(data['testToken'], self.user)
        self.assertEqual(data['testOtherToken'], self.other_user)

        self.assertIsNone(data['testInvalidToken'])
        self.assertEqual(len(response.errors), 1)

    @override_jwt_settings(
        JWT_ALLOW_ARGUMENT=True,
        JWT_ALLOW_ANY_CLASSES=[
            'graphene.types.generic.GenericScalar',
        ])
    def test_allow_any(self):
        query = '''
        {{
          testAllowAny: test
          testInvalidToken: test({0}: "invalid")
        }}'''.format(jwt_settings.JWT_ARGUMENT_NAME)

        headers = {
            jwt_settings.JWT_AUTH_HEADER_NAME: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                'invalid',
            ),
        }

        response = self.client.execute(query, **headers)

        self.assertIsInstance(response.data['testAllowAny'], AnonymousUser)
        self.assertIsInstance(response.data['testInvalidToken'], AnonymousUser)
