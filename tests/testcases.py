from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, testcases

import graphene
from graphene.types.generic import GenericScalar

from graphql_jwt.utils import jwt_encode, jwt_payload


class GraphQLRequestFactory(RequestFactory):

    def execute(self, query, **variables):
        return self._schema.execute(query, variable_values=variables)


class GraphQLClient(GraphQLRequestFactory, Client):

    def __init__(self, **defaults):
        super(GraphQLClient, self).__init__(**defaults)
        self._schema = None

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)


class UserTestCase(testcases.TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test',
            password='dolphins')


class GraphQLJWTTestCase(UserTestCase):

    def setUp(self):
        super(GraphQLJWTTestCase, self).setUp()

        self.payload = jwt_payload(self.user)
        self.token = jwt_encode(self.payload)
        self.factory = RequestFactory()


class GraphQLSchemaTestCase(GraphQLJWTTestCase):

    class Query(graphene.ObjectType):
        test = GenericScalar()

    Mutations = None
    client_class = GraphQLClient

    def setUp(self):
        super(GraphQLSchemaTestCase, self).setUp()
        self.client.schema(query=self.Query, mutation=self.Mutations)
