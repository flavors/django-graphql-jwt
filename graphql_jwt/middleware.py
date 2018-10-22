from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

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

    def process_request(self, request):
        if get_authorization_header(request) is not None:
            if not hasattr(request, 'user') or request.user.is_anonymous:
                try:
                    user = authenticate(request=request)
                except JSONWebTokenError as err:
                    return JsonResponse({
                        'errors': [{'message': str(err)}],
                    }, status=401)

                if user is not None:
                    request.user = request._cached_user = user

    def process_response(self, request, response):
        patch_vary_headers(response, ('Authorization',))
        return response
