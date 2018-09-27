from django.contrib.auth import get_user_model
from django.test import RequestFactory, testcases

import graphene
from graphene.types.generic import GenericScalar

from graphql_jwt.testcases import JSONWebTokenTestCase
from graphql_jwt.utils import jwt_encode, jwt_payload


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
        self.factory = RequestFactory()


class SchemaTestCase(TestCase, JSONWebTokenTestCase):

    class Query(graphene.ObjectType):
        test = GenericScalar()

    Mutations = None

    def setUp(self):
        super(SchemaTestCase, self).setUp()
        self.client.schema(query=self.Query, mutation=self.Mutations)
