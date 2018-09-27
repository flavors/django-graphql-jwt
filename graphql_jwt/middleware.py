from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin

from .exceptions import JSONWebTokenError
from .utils import get_authorization_header


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
