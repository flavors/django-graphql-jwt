import warnings

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from graphene_django.settings import graphene_settings

from .exceptions import JSONWebTokenError
from .settings import jwt_settings
from .utils import get_authorization_header, get_credentials

__all__ = [
    'allow_any',
    'JSONWebTokenMiddleware',
]


def allow_any(info, **kwargs):
    field = getattr(
        info.schema,
        'get_{}_type'.format(info.operation.operation),
    )().fields.get(info.field_name)

    if field is None:
        return False

    graphene_type = getattr(field.type, 'graphene_type', None)

    return graphene_type is not None and\
        issubclass(graphene_type, tuple(jwt_settings.JWT_ALLOW_ANY_CLASSES))


class DjangoMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        if JSONWebTokenMiddleware not in graphene_settings.MIDDLEWARE:
            warnings.warn(
                'You do not have '
                '\'graphql_jwt.middleware.JSONWebTokenMiddleware\' '
                'in your GRAPHENE[\'MIDDLEWARE\'] setting. '
                'Please see the documentation for more information: '
                '<https://github.com/flavors/django-graphql-jwt#installation>',
                stacklevel=2)

        super(JSONWebTokenMiddleware, self).__init__(get_response)

    def process_request(self, request):
        if (get_authorization_header(request) is not None and
                (not hasattr(request, 'user') or request.user.is_anonymous)):
            try:
                user = authenticate(request=request)
            except JSONWebTokenError as err:
                return JsonResponse({
                    'errors': [{'message': str(err)}],
                }, status=401)

            if user is not None:
                request.user = request._cached_user = user
        return None

    def process_response(self, request, response):
        patch_vary_headers(response, ('Authorization',))
        return response


class JSONWebTokenMiddleware(DjangoMiddleware):

    def __init__(self, get_response=None):
        self.cached_allow_any = set()
        super(JSONWebTokenMiddleware, self).__init__(get_response)

    def authenticate_context(self, info, **kwargs):
        root_path = info.path[0]

        if root_path not in self.cached_allow_any:
            if jwt_settings.JWT_ALLOW_ANY_HANDLER(info, **kwargs):
                self.cached_allow_any.add(root_path)
            else:
                return True
        return False

    def resolve(self, next, root, info, **kwargs):
        context = info.context

        if (get_credentials(context, **kwargs) is not None and
                (not hasattr(context, 'user') or context.user.is_anonymous)):

            if self.authenticate_context(info, **kwargs):
                user = authenticate(request=context, **kwargs)

                if user is not None:
                    context.user = context._cached_user = user

        return next(root, info, **kwargs)
