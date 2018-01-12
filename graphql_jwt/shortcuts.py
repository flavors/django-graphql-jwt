from .utils import get_payload, get_user_by_payload, jwt_encode, jwt_payload


def get_token(user, **extra):
    payload = jwt_payload(user)
    payload.update(extra)
    return jwt_encode(payload)


def get_user_by_token(token):
    payload = get_payload(token)
    return get_user_by_payload(payload)
