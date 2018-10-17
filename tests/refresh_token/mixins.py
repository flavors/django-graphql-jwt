import graphene

from graphql_jwt.shortcuts import create_refresh_token, get_refresh_token
from graphql_jwt.utils import get_payload

from ..decorators import override_jwt_settings
from ..mixins import back_to_the_future, refresh_expired


class LongRunningRefreshMixin(object):

    @override_jwt_settings(JWT_LONG_RUNNING_REFRESH_TOKEN=True)
    def setUp(self):
        self.Mutations = type('jwt', (graphene.ObjectType,), {
            name: mutation.Field() for name, mutation in
            self.refresh_token_mutations.items()
        })

        super(LongRunningRefreshMixin, self).setUp()


class TokenAuthMixin(LongRunningRefreshMixin):

    @override_jwt_settings(JWT_LONG_RUNNING_REFRESH_TOKEN=True)
    def test_token_auth(self):
        response = self.execute({
            'username': self.user.get_username(),
            'password': 'dolphins',
        })

        data = response.data['tokenAuth']
        payload = get_payload(data['token'])
        refresh_token = get_refresh_token(data['refreshToken'])

        self.assertEqual(self.user.get_username(), payload['username'])
        self.assertEqual(refresh_token.user, self.user)


class RefreshTokenMixin(object):

    def setUp(self):
        super(RefreshTokenMixin, self).setUp()
        self.refresh_token = create_refresh_token(self.user)


class RefreshMixin(LongRunningRefreshMixin, RefreshTokenMixin):

    def test_refresh_token(self):
        with back_to_the_future(seconds=1):
            response = self.execute({
                'refreshToken': self.refresh_token.token,
            })

        data = response.data['refreshToken']
        token = data['token']
        refresh_token = get_refresh_token(data['refreshToken'])

        self.assertNotEqual(token, self.token)
        self.assertNotEqual(refresh_token.token, self.refresh_token.token)
        self.assertEqual(refresh_token.user, self.user)

        payload = get_payload(token)
        self.assertGreater(payload['exp'], self.payload['exp'])

    def test_refresh_token_expired(self):
        with refresh_expired():
            response = self.execute({
                'refreshToken': self.refresh_token.token,
            })

        self.assertTrue(response.errors)


class RevokeMixin(RefreshTokenMixin):

    def test_revoke(self):
        response = self.execute({
            'refreshToken': self.refresh_token.token,
        })

        self.refresh_token.refresh_from_db()

        self.assertIsNotNone(self.refresh_token.revoked)
        self.assertTrue(response.data['revokeToken']['revoked'])