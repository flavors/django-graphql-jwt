from django.contrib.auth import authenticate
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

from graphene_django.settings import graphene_settings


class SchemaRequestFactory(RequestFactory):

    def execute(self, context, query, variables):
        return self._schema.execute(
            query,
            context=context,
            variables=variables)


class GraphQLJWTClient(SchemaRequestFactory, Client):

    def __init__(self, **defaults):
        super(GraphQLJWTClient, self).__init__(**defaults)
        self._credentials = {}
        self._schema = graphene_settings.SCHEMA

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))
        request.user = authenticate(request)
        return request

    def credentials(self, **kwargs):
        self._credentials = kwargs

    def execute(self, query, variables=None, **extra):
        extra.update(self._credentials)
        context = self.post('/', **extra)
        return super(GraphQLJWTClient, self).execute(context, query, variables)

    def logout(self):
        self._credentials.pop('HTTP_AUTHORIZATION', None)


class GraphQLJWTTestCase(testcases.TestCase):
    client_class = GraphQLJWTClient
