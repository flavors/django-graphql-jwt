from calendar import timegm
from datetime import datetime

from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

import jwt

from . import settings
from .exceptions import GraphQLJWTError


def jwt_payload(user):
    username = user.get_username()

    if hasattr(username, 'pk'):
        username = username.pk

    payload = {
        user.USERNAME_FIELD: username,
        'exp': datetime.utcnow() + settings.JWT_EXPIRATION_DELTA,
    }

    if settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())

    if settings.JWT_AUDIENCE is not None:
        payload['aud'] = settings.JWT_AUDIENCE

    if settings.JWT_ISSUER is not None:
        payload['iss'] = settings.JWT_ISSUER

    return payload


def jwt_encode(payload):
    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        settings.JWT_ALGORITHM,
    ).decode('utf-8')


def jwt_decode(token):
    return jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        settings.JWT_VERIFY,
        options={
            'verify_exp': settings.JWT_VERIFY_EXPIRATION,
        },
        leeway=settings.JWT_LEEWAY,
        audience=settings.JWT_AUDIENCE,
        issuer=settings.JWT_ISSUER,
        algorithms=[settings.JWT_ALGORITHM])


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', '').split()
    prefix = settings.JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2 or auth[0].lower() != prefix.lower():
        return None
    return auth[1]


def get_payload(token):
    try:
        payload = jwt_decode(token)
    except jwt.ExpiredSignature:
        raise GraphQLJWTError(_('Signature has expired'))
    except jwt.DecodeError:
        raise GraphQLJWTError(_('Error decoding signature'))
    except jwt.InvalidTokenError:
        raise GraphQLJWTError(_('Invalid token'))
    return payload


def get_user_by_natural_key(user_id):
    User = get_user_model()
    try:
        return User.objects.get_by_natural_key(user_id)
    except User.DoesNotExist:
        return None


def get_user_by_payload(payload):
    username = payload.get(get_user_model().USERNAME_FIELD)

    if not username:
        raise GraphQLJWTError(_('Invalid payload'))

    user = get_user_by_natural_key(username)

    if user is not None and not user.is_active:
        raise GraphQLJWTError(_('User is disabled'))
    return user
