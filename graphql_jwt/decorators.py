from datetime import datetime
from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import ugettext as _

from graphql.execution.base import ResolveInfo
from promise import Promise, is_thenable

from . import exceptions, signals
from .refresh_token.shortcuts import refresh_token_lazy
from .settings import jwt_settings
from .shortcuts import get_token

__all__ = [
    'user_passes_test',
    'login_required',
    'staff_member_required',
    'permission_required',
    'token_auth',
    'setup_jwt_cookie',
    'jwt_cookie',
]


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator


def user_passes_test(test_func, exc=exceptions.PermissionDenied()):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context.user):
                return f(*args, **kwargs)
            raise exc
        return wrapper
    return decorator


login_required = user_passes_test(lambda u: u.is_authenticated)
staff_member_required = user_passes_test(lambda u: u.is_active and u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_active and u.is_superuser)


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm

        if user.has_perms(perms):
            return True
        return False
    return user_passes_test(check_perms)


def token_auth(f):
    @wraps(f)
    @setup_jwt_cookie
    def wrapper(cls, root, info, password, **kwargs):
        context = info.context
        context._jwt_token_auth = True

        def on_resolve(values):
            user, payload = values
            payload.token = get_token(user, context)

            if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
                payload.refresh_token = refresh_token_lazy(user)

            return payload

        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=context,
            username=username,
            password=password,
        )

        if user is None:
            raise exceptions.JSONWebTokenError(
                _('Please, enter valid credentials'))

        if hasattr(context, 'user'):
            context.user = user

        result = f(cls, root, info, **kwargs)
        values = (user, result)

        signals.token_issued.send(sender=cls, request=context, user=user)

        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper


def setup_jwt_cookie(f):
    @wraps(f)
    def wrapper(cls, root, info, *args, **kwargs):
        result = f(cls, root, info, **kwargs)

        if getattr(info.context, 'jwt_cookie', False):
            info.context.jwt_token = result.token
        return result
    return wrapper


def jwt_cookie(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        request.jwt_cookie = True
        response = view_func(request, *args, **kwargs)

        if hasattr(request, 'jwt_token'):
            expires = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA

            response.set_cookie(
                jwt_settings.JWT_COOKIE_NAME,
                request.jwt_token,
                expires=expires,
                httponly=True,
                secure=jwt_settings.JWT_COOKIE_SECURE,
            )
            if hasattr(request, 'jwt_refresh_token'):
                refresh_token = request.jwt_refresh_token
                expires = refresh_token.created +\
                    jwt_settings.JWT_REFRESH_EXPIRATION_DELTA

                response.set_cookie(
                    jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
                    refresh_token.token,
                    expires=expires,
                    httponly=True,
                    secure=jwt_settings.JWT_COOKIE_SECURE,
                )
        return response
    return wrapped_view
