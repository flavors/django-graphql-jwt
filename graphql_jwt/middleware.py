import warnings

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from graphene_django.settings import graphene_settings

from . import mixins
from .exceptions import JSONWebTokenError
from .refresh_token import mixins as refresh_token_mixins
from .settings import jwt_settings
from .utils import get_authorization_header


def is_authenticated(info, field, **kwargs):
    return not issubclass(field.type.graphene_type, (
        mixins.JSONWebTokenMixin,
        mixins.VerifyMixin,
        refresh_token_mixins.RevokeMixin))


class JSONWebTokenMiddleware(MiddlewareMixin):

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

    def resolve(self, next, root, info, **kwargs):
        context = info.context

        if (get_authorization_header(context) is not None and
                (not hasattr(context, 'user') or context.user.is_anonymous)):

            field = getattr(
                info.schema,
                'get_{}_type'.format(info.operation.operation),
            )().fields.get(info.path[0])

            is_authenticated = jwt_settings.JWT_IS_AUTHENTICATED_HANDLER

            if field is None or is_authenticated(info, field, **kwargs):
                user = authenticate(request=context)

                if user is not None:
                    context.user = context._cached_user = user

        return next(root, info, **kwargs)
