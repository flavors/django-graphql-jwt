from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from promise import Promise, is_thenable

from . import exceptions
from .shortcuts import get_token

__all__ = [
    'login_required',
    'staff_member_required',
    'permission_required',
    'token_auth',
]


def context(f):
    def _context(func):
        def wrapper(*args, **kwargs):
            info = args[f.__code__.co_varnames.index('info')]
            return func(info.context, *args, **kwargs)
        return wrapper
    return _context


def login_required(f):
    @wraps(f)
    @context(f)
    def wrapper(context, *args, **kwargs):
        if context.user.is_anonymous:
            raise exceptions.PermissionDenied()
        return f(*args, **kwargs)
    return wrapper


def staff_member_required(f):
    @wraps(f)
    @context(f)
    def wrapper(context, *args, **kwargs):
        user = context.user
        if user.is_active and user.is_staff:
            return f(*args, **kwargs)
        raise exceptions.PermissionDenied()
    return wrapper


def permission_required(perm):
    def check_perms(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if isinstance(perm, six.string_types):
                perms = (perm,)
            else:
                perms = perm

            if not context.user.has_perms(perms):
                raise exceptions.PermissionDenied()
            return f(*args, **kwargs)
        return wrapper
    return check_perms


def token_auth(f):
    @wraps(f)
    def wrapper(cls, root, info, password, **kwargs):
        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user)
            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=info.context,
            username=username,
            password=password)

        if user is None:
            raise exceptions.GraphQLJWTError(
                _('Please, enter valid credentials'))

        if hasattr(info.context, 'user'):
            info.context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        # Improved mutation with thenable check
        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper
