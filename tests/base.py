from django.contrib.auth import get_user_model
from django.test import Client, RequestFactory, testcases

from graphene_django.settings import graphene_settings
from graphql_jwt.utils import jwt_payload, jwt_encode


class GraphQLRequestFactory(RequestFactory):

    def execute(self, query, **kwargs):
        return self.schema.execute(query, variable_values=kwargs)


class GraphQLClient(GraphQLRequestFactory, Client):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self.schema = graphene_settings.SCHEMA


class GraphQLJWTTestCase(testcases.TestCase):
    client_class = GraphQLClient

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test')
        self.payload = jwt_payload(self.user)
        self.token = jwt_encode(self.payload)
        self.factory = RequestFactory()
