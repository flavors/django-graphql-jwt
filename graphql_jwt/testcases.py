from django.contrib.auth import authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

import graphene
from graphene_django.settings import graphene_settings

from .settings import jwt_settings
from .shortcuts import get_token


class SchemaRequestFactory(RequestFactory):

    def __init__(self, **defaults):
        super(SchemaRequestFactory, self).__init__(**defaults)
        self._schema = graphene_settings.SCHEMA

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def execute(self, context, query, variables):
        return self._schema.execute(
            query,
            context=context,
            variables=variables)


class JSONWebTokenClient(SchemaRequestFactory, Client):

    def __init__(self, **defaults):
        super(JSONWebTokenClient, self).__init__(**defaults)
        self._credentials = {}

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))
        request.user = authenticate(request)
        return request

    def credentials(self, **kwargs):
        self._credentials = kwargs

    def execute(self, query, variables=None, **extra):
        extra.update(self._credentials)
        context = self.post('/', **extra)
        return super(JSONWebTokenClient, self)\
            .execute(context, query, variables)

    def authenticate(self, user):
        self._credentials = {
            jwt_settings.JWT_AUTH_HEADER: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                get_token(user)),
        }

    def logout(self):
        self._credentials.pop(jwt_settings.JWT_AUTH_HEADER, None)


class JSONWebTokenTestCase(testcases.TestCase):
    client_class = JSONWebTokenClient
