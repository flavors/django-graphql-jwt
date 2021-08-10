import json
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

import graphene
from graphene_django.views import GraphQLView

from graphql_jwt.compat import GraphQLResolveInfo
from graphql_jwt.decorators import jwt_cookie
from graphql_jwt.settings import jwt_settings
from graphql_jwt.testcases import JSONWebTokenClient, JSONWebTokenTestCase
from graphql_jwt.utils import jwt_encode, jwt_payload


class UserTestCase(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test",
            password="dolphins",
        )


class TestCase(UserTestCase):
    def setUp(self):
        super().setUp()
        self.payload = jwt_payload(self.user)
        self.token = jwt_encode(self.payload)
        self.request_factory = RequestFactory()

    def info(self, user=None, **headers):
        request = self.request_factory.post("/", **headers)

        if user is not None:
            request.user = user

        return mock.Mock(
            context=request,
            path=["test"],
            spec=GraphQLResolveInfo,
        )


class SchemaTestCase(TestCase, JSONWebTokenTestCase):
    class Query(graphene.ObjectType):
        test = graphene.String()

    Mutation = None

    def setUp(self):
        super().setUp()
        self.client.schema(query=self.Query, mutation=self.Mutation)

    def execute(self, variables=None):
        assert self.query, "`query` property not specified"
        return self.client.execute(self.query, variables)

    def assertUsernameIn(self, payload):
        username = payload[self.user.USERNAME_FIELD]
        self.assertEqual(self.user.get_username(), username)


class RelaySchemaTestCase(SchemaTestCase):
    def execute(self, variables=None):
        return super().execute({"input": variables})


class CookieClient(JSONWebTokenClient):
    def post(self, path, data, **kwargs):
        kwargs.setdefault("content_type", "application/json")
        return self.generic("POST", path, json.dumps(data), **kwargs)

    def set_cookie(self, token):
        self.cookies[jwt_settings.JWT_COOKIE_NAME] = token

    def execute(self, query, variables=None, **extra):
        data = {
            "query": query,
            "variables": variables,
        }
        view = GraphQLView(schema=self._schema)
        request = self.post("/", data=data, **extra)
        response = jwt_cookie(view.dispatch)(request)
        content = self._parse_json(response)
        response.data = content.get("data")
        response.errors = content.get("errors")
        return response


class CookieTestCase(SchemaTestCase):
    client_class = CookieClient

    def set_cookie(self):
        self.client.set_cookie(self.token)


class RelayCookieTestCase(RelaySchemaTestCase, CookieTestCase):
    """RelayCookieTestCase"""
