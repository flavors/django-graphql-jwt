from datetime import datetime, timedelta
from unittest.mock import patch

from graphql_jwt import settings
from graphql_jwt.utils import jwt_encode

from .base import GraphQLJWTTestCase


class MutationsTests(GraphQLJWTTestCase):

    def test_verify(self):
        query = '''
        mutation VerifyToken($token: String!) {
          verifyToken(token: $token) {
            payload
          }
        }'''

        response = self.client.execute(query, token=self.token)
        payload = response.data['verifyToken']['payload']

        self.assertEqual(self.user.username, payload['username'])

    def test_verify_invalid_token(self):
        query = '''
        mutation VerifyToken($token: String!) {
          verifyToken(token: $token) {
            payload
          }
        }'''

        response = self.client.execute(query, token='invalid')
        self.assertTrue(response.errors)

    def test_refresh(self):
        query = '''
        mutation RefreshToken($token: String!) {
          refreshToken(token: $token) {
            data
          }
        }'''

        with patch('graphql_jwt.utils.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value =\
                datetime.utcnow() + timedelta(seconds=1)

            response = self.client.execute(query, token=self.token)

        data = response.data['refreshToken']['data']

        self.assertNotEqual(self.token, data['token'])
        self.assertEqual(self.user.username, data['payload']['username'])

    def test_refresh_expired(self):
        query = '''
        mutation RefreshToken($token: String!) {
          refreshToken(token: $token) {
            data
          }
        }'''

        with patch('graphql_jwt.mutations.datetime') as datetime_mock:
            datetime_mock.utcnow.return_value = datetime.utcnow() +\
                settings.JWT_REFRESH_EXPIRATION_DELTA +\
                timedelta(seconds=1)

            response = self.client.execute(query, token=self.token)

        self.assertTrue(response.errors)

    def test_refresh_error(self):
        del self.payload['orig_iat']
        token = jwt_encode(self.payload)

        query = '''
        mutation RefreshToken($token: String!) {
          refreshToken(token: $token) {
            data
          }
        }'''

        response = self.client.execute(query, token=token)
        self.assertTrue(response.errors)
