from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.utils.cache import patch_vary_headers

from .exceptions import GraphQLJWTError
from .utils import get_authorization_header


class JSONWebTokenMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if get_authorization_header(request) is not None:
            if not hasattr(request, 'user') or request.user.is_anonymous:
                try:
                    user = authenticate(request=request)
                except GraphQLJWTError as err:
                    return JsonResponse({
                        'errors': [{'message': str(err)}],
                    }, status=401)

                if user is not None:
                    request.user = request._cached_user = user

        response = self.get_response(request)
        patch_vary_headers(response, ('Authorization',))
        return response
