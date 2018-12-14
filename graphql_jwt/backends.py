from .refresh_token.blacklist import is_in_blacklist
from .settings import jwt_settings
from .shortcuts import get_user_by_token
from .utils import get_credentials, get_payload, get_user_by_natural_key


class JSONWebTokenBackend(object):

    def authenticate(self, request=None, **kwargs):
        if request is None:
            return None

        token = get_credentials(request, **kwargs)

        if token is not None:
            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                refresh_token = get_payload(token)['refresh_token']
                if is_in_blacklist(refresh_token):
                    return None
            return get_user_by_token(token, request)

        return None

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)
