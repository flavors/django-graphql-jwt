from django.contrib.auth.models import AnonymousUser
from django.core.handlers.wsgi import WSGIRequest
from django.test import Client, RequestFactory, testcases

import graphene
from graphene_django.settings import graphene_settings
from graphene.test import format_execution_result, default_format_error

from .middleware import JSONWebTokenMiddleware
from .settings import jwt_settings
from .shortcuts import get_token

from promise import Promise, is_thenable


class SchemaRequestFactory(RequestFactory):

    def __init__(self, **defaults):
        super().__init__(**defaults)
        self._schema = graphene_settings.SCHEMA
        self._middleware = [JSONWebTokenMiddleware]

    def schema(self, **kwargs):
        self._schema = graphene.Schema(**kwargs)

    def middleware(self, middleware):
        self._middleware = middleware

    def execute(self, query, **options):
        options.setdefault('middleware', [m() for m in self._middleware])
        return self._schema.execute(query, **options)


class JSONWebTokenClient(SchemaRequestFactory, Client):

    def __init__(self, format_error=None, **defaults):
        self.format_error = format_error or default_format_error
        super().__init__(**defaults)
        self._credentials = {}

    def request(self, **request):
        request = WSGIRequest(self._base_environ(**request))
        request.user = AnonymousUser()
        return request

    def credentials(self, **kwargs):
        self._credentials = kwargs

    def format_result(self, result):
        return format_execution_result(result, self.format_error)

    def execute(self, query, variables=None, **extra):
        extra.update(self._credentials)
        context = self.post('/', **extra)

        executed = super().execute(
            query,
            context_value=context,
            variable_values=variables,
        )

        if is_thenable(executed):
            return Promise.resolve(executed).then(self.format_result)
        return self.format_result(executed)

    def authenticate(self, user):
        self._credentials = {
            jwt_settings.JWT_AUTH_HEADER_NAME: '{0} {1}'.format(
                jwt_settings.JWT_AUTH_HEADER_PREFIX,
                get_token(user)),
        }

    def logout(self):
        self._credentials.pop(jwt_settings.JWT_AUTH_HEADER_NAME, None)


class JSONWebTokenTestCase(testcases.TestCase):
    client_class = JSONWebTokenClient
