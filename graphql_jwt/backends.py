from .shortcuts import get_user_by_token
from .utils import get_authorization_header, get_user_by_natural_key


class JSONWebTokenBackend(object):

    def authenticate(self, request=None, **credentials):
        if request is None:
            return None

        token = get_authorization_header(request)

        if token is not None:
            return get_user_by_token(token, request)

        return None

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)
