from .utils import (
    get_authorization_header,
    get_user_by_token,
    get_user_by_natural_key
)


class JWTBackend(object):

    def authenticate(self, request=None, **credentials):
        if request is None:
            return None

        token = get_authorization_header(request)
        return get_user_by_token(token)

    def get_user(self, user_id):
        return get_user_by_natural_key(user_id)
