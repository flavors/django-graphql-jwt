from functools import wraps

from django.contrib.auth import authenticate, get_user_model, login
from django.utils.translation import ugettext_lazy as _

from promise import Promise, is_thenable

from . import exceptions
from .shortcuts import get_token


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

        login(info.context, user)
        result = f(cls, root, info, **kwargs)
        values = (user, result)

        # Improved mutation with thenable check
        if is_thenable(result):
            return Promise.resolve(values).then(on_resolve)
        return on_resolve(values)
    return wrapper
