from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.utils import six
from django.utils.translation import ugettext as _

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
                payload.refresh_token = create_refresh_token(user).token

            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        if get_authorization_header(info.context) is not None:
            del info.context.META[jwt_settings.JWT_AUTH_HEADER]

        user = authenticate(
            request=info.context,
            username=username,
            password=password)

        if user is None:
            raise exceptions.JSONWebTokenError(
                _('Please, enter valid credentials'))

        if hasattr(info.context, 'user'):
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper
