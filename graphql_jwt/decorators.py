from calendar import timegm
from datetime import datetime
from functools import wraps

from django.contrib.auth import authenticate, get_user_model
from django.middleware.csrf import rotate_token
from django.utils.translation import gettext as _

from graphene.utils.thenables import maybe_thenable

from . import exceptions, signals
from .compat import GraphQLResolveInfo
from .refresh_token.shortcuts import create_refresh_token, refresh_token_lazy
from .settings import jwt_settings
from .utils import delete_cookie, set_cookie

__all__ = [
    "user_passes_test",
    "login_required",
    "staff_member_required",
    "superuser_required",
    "permission_required",
    "token_auth",
    "csrf_rotation",
    "setup_jwt_cookie",
    "jwt_cookie",
    "ensure_token",
]


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, GraphQLResolveInfo))
            return func(info.context, *args, **kwargs)

        return wrapper

    return decorator


def user_passes_test(test_func, exc=exceptions.PermissionDenied):
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
staff_member_required = user_passes_test(lambda u: u.is_staff)
superuser_required = user_passes_test(lambda u: u.is_superuser)


def permission_required(perm):
    def check_perms(user):
        if isinstance(perm, str):
            perms = (perm,)
        else:
            perms = perm
        return user.has_perms(perms)

    return user_passes_test(check_perms)


def on_token_auth_resolve(values):
    context, user, payload = values
    payload.payload = jwt_settings.JWT_PAYLOAD_HANDLER(user, context)
    payload.token = jwt_settings.JWT_ENCODE_HANDLER(payload.payload, context)

    if jwt_settings.JWT_LONG_RUNNING_REFRESH_TOKEN:
        if getattr(context, "jwt_cookie", False):
            context.jwt_refresh_token = create_refresh_token(user)
            payload.refresh_token = context.jwt_refresh_token.get_token()
        else:
            payload.refresh_token = refresh_token_lazy(user)

    return payload


def token_auth(f):
    @wraps(f)
    @setup_jwt_cookie
    @csrf_rotation
    @refresh_expiration
    def wrapper(cls, root, info, password, **kwargs):
        context = info.context
        context._jwt_token_auth = True
        username = kwargs.get(get_user_model().USERNAME_FIELD)

        user = authenticate(
            request=context,
            username=username,
            password=password,
        )
        if user is None:
            raise exceptions.JSONWebTokenError(
                _("Please enter valid credentials"),
            )

        if hasattr(context, "user"):
            context.user = user

        result = f(cls, root, info, **kwargs)
        signals.token_issued.send(sender=cls, request=context, user=user)
        return maybe_thenable((context, user, result), on_token_auth_resolve)

    return wrapper


def refresh_expiration(f):
    @wraps(f)
    def wrapper(cls, *args, **kwargs):
        def on_resolve(payload):
            payload.refresh_expires_in = (
                timegm(datetime.utcnow().utctimetuple())
                + jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
            )
            return payload

        result = f(cls, *args, **kwargs)
        return maybe_thenable(result, on_resolve)

    return wrapper


def csrf_rotation(f):
    @wraps(f)
    def wrapper(cls, root, info, *args, **kwargs):
        result = f(cls, root, info, **kwargs)

        if jwt_settings.JWT_CSRF_ROTATION:
            rotate_token(info.context)
        return result

    return wrapper


def setup_jwt_cookie(f):
    @wraps(f)
    def wrapper(cls, root, info, *args, **kwargs):
        result = f(cls, root, info, **kwargs)

        if getattr(info.context, "jwt_cookie", False):
            info.context.jwt_token = result.token
        return result

    return wrapper


def jwt_cookie(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        request.jwt_cookie = True
        response = view_func(request, *args, **kwargs)

        if hasattr(request, "jwt_token"):
            expires = datetime.utcnow() + jwt_settings.JWT_EXPIRATION_DELTA

            set_cookie(
                response,
                jwt_settings.JWT_COOKIE_NAME,
                request.jwt_token,
                expires=expires,
            )
            if hasattr(request, "jwt_refresh_token"):
                refresh_token = request.jwt_refresh_token
                expires = (
                    refresh_token.created + jwt_settings.JWT_REFRESH_EXPIRATION_DELTA
                )

                set_cookie(
                    response,
                    jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME,
                    refresh_token.token,
                    expires=expires,
                )

        if hasattr(request, "delete_jwt_cookie"):
            delete_cookie(response, jwt_settings.JWT_COOKIE_NAME)

        if hasattr(request, "delete_refresh_token_cookie"):
            delete_cookie(response, jwt_settings.JWT_REFRESH_TOKEN_COOKIE_NAME)

        return response

    return wrapped_view


def ensure_token(f):
    @wraps(f)
    def wrapper(cls, root, info, token=None, *args, **kwargs):
        if token is None:
            token = info.context.COOKIES.get(jwt_settings.JWT_COOKIE_NAME)

            if token is None:
                raise exceptions.JSONWebTokenError(_("Token is required"))
        return f(cls, root, info, token, *args, **kwargs)

    return wrapper
