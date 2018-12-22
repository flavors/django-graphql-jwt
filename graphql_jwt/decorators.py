from functools import wraps

from defender import utils

from django.contrib.auth import authenticate, get_user_model
from django.utils import six

from promise import Promise, is_thenable

from . import exceptions
from .refresh_token.shortcuts import create_refresh_token
from .settings import jwt_settings
from .shortcuts import get_token
from .utils import get_authorization_header

__all__ = [
    'user_passes_test',
    'login_required',
    'staff_member_required',
    'permission_required',
    'token_auth',
]


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator


def user_passes_test(test_func):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exceptions.PermissionDenied()
        return wrapper
    return decorator


login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_active and u.is_superuser)


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, six.string_types):
            perms = (perm,)
        else:
            perms = perm

        if user.has_perms(perms):
            return True
        return False
    return user_passes_test(check_perms)


def token_auth(f):
    @wraps(f)
    def wrapper(cls, root, info, password, **kwargs):
        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user, info.context)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                payload.refresh_token = create_refresh_token(user).get_token()

            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        if get_authorization_header(info.context) is not None:
            del info.context.META[jwt_settings.JWT_AUTH_HEADER_NAME]

        if jwt_settings.DJANGO_DEFENDER_BRUTE_FORCE_PROTECTION:
            if utils.is_already_locked(request=info.context, username=username):
                raise exceptions.JSONWebTokenError(
                    jwt_settings.DJANGO_DEFENDER_LOCK_MESSAGE
                )

        user = authenticate(request=info.context, username=username, password=password)

        login_valid = bool(user)
        user_blocked = False

        if jwt_settings.DJANGO_DEFENDER_BRUTE_FORCE_PROTECTION:
            utils.add_login_attempt_to_db(
                request=info.context, login_valid=login_valid, username=username
            )

            user_blocked = not utils.check_request(
                request=info.context,
                login_unsuccessful=not login_valid,
                username=username,
            )

        if not login_valid or user_blocked:
            raise exceptions.JSONWebTokenError(jwt_settings.JWT_CRED_FAIL_MESSAGE)

        if hasattr(info.context, 'user'):
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper
