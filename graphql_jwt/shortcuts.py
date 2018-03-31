from .settings import jwt_settings
from .utils import get_payload, get_user_by_payload


def get_token(user, **extra):
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    payload.update(extra)
    return jwt_settings.JWT_ENCODE_HANDLER(payload)


def get_user_by_token(token):
    payload = get_payload(token)
    return get_user_by_payload(payload)
