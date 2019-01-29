from django.contrib.auth import get_user_model
from django.test import RequestFactory, testcases

from graphql.execution.base import ResolveInfo

from graphql_jwt.testcases import JSONWebTokenTestCase
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


class RelaySchemaTestCase(SchemaTestCase):

    def execute(self, variables=None):
        return super(RelaySchemaTestCase, self).execute({'input': variables})
