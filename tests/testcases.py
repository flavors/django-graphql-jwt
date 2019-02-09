import json

from django.contrib.auth import get_user_model
from django.test import RequestFactory, testcases

from graphene_django.views import GraphQLView
from graphql.execution.base import ResolveInfo

from graphql_jwt.decorators import jwt_cookie
from graphql_jwt.settings import jwt_settings
from graphql_jwt.testcases import JSONWebTokenClient, JSONWebTokenTestCase
from graphql_jwt.utils import jwt_encode, jwt_payload

from .compat import mock


class UserTestCase(testcases.TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins')


class TestCase(UserTestCase):

    def setUp(self):
        super(TestCase, self).setUp()

        self.payload = jwt_payload(self.user)
        self.token = jwt_encode(self.payload)
        self.request_factory = RequestFactory()

    def info(self, user=None, **headers):
        request = self.request_factory.post('/', **headers)

        if user is not None:
            request.user = user

        return mock.Mock(context=request, path=['test'], spec=ResolveInfo)


class SchemaTestCase(TestCase, JSONWebTokenTestCase):
    Query = None
    Mutation = None

    def setUp(self):
        super(SchemaTestCase, self).setUp()
        self.client.schema(query=self.Query, mutation=self.Mutation)

    def execute(self, variables=None):
        assert self.query, ('`query` property not specified')
        return self.client.execute(self.query, variables)

    def assertUsernameIn(self, payload):
        username = payload[self.user.USERNAME_FIELD]
        self.assertEqual(self.user.get_username(), username)


class RelaySchemaTestCase(SchemaTestCase):

    def execute(self, variables=None):
        return super(RelaySchemaTestCase, self).execute({'input': variables})


class CookieGraphQLViewClient(JSONWebTokenClient):

    def post(self, path, data, **kwargs):
        data = json.dumps(data)
        kwargs.setdefault('content_type', 'application/json')
        return self.generic('POST', path, data, **kwargs)

    def authenticate(self, token):
        self.cookies[jwt_settings.JWT_COOKIE_KEY] = token

    def execute(self, query, variables=None, **extra):
        data = {
            'query': query,
            'variables': variables,
        }

        view = GraphQLView(schema=self._schema)
        request = self.post('/', data=data, **extra)
        response = jwt_cookie(view.dispatch)(request)
        response.data = self._parse_json(response)['data']
        return response


class CookieGraphQLViewTestCase(SchemaTestCase):
    client_class = CookieGraphQLViewClient

    def authenticate(self):
        self.client.authenticate(self.token)
