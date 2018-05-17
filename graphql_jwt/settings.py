from datetime import timedelta
from importlib import import_module

from django.conf import settings
from django.test.signals import setting_changed
from django.utils import six

import environ


class Env(environ.Env):

    def timedelta(self, var, default=environ.Env.NOTSET):

        def cast(value):
            args = [val.split('=') for val in value.split(',') if val]
            return timedelta(**{name: float(val) for name, val in args})

        return self.get_value(var, cast=cast, default=default)


env = Env()

DEFAULTS = {
    'JWT_ALGORITHM': env('JWT_ALGORITHM', default='HS256'),
    'JWT_AUDIENCE': env('JWT_AUDIENCE', default=None),
    'JWT_AUTH_HEADER': env('JWT_AUTH_HEADER', default='HTTP_AUTHORIZATION'),
    'JWT_AUTH_HEADER_PREFIX': env('JWT_AUTH_HEADER_PREFIX', default='JWT'),
    'JWT_ISSUER': env('JWT_ISSUER', default=None),
    'JWT_LEEWAY': env.timedelta('JWT_LEEWAY', 0),
    'JWT_SECRET_KEY': env('JWT_SECRET_KEY', default=settings.SECRET_KEY),
    'JWT_VERIFY': env.bool('JWT_VERIFY', True),
    'JWT_VERIFY_EXPIRATION': env.bool('JWT_VERIFY_EXPIRATION', False),

    'JWT_EXPIRATION_DELTA': env.timedelta(
        'JWT_EXPIRATION_DELTA',
        timedelta(seconds=60 * 5)),

    'JWT_ALLOW_REFRESH': env.bool('JWT_ALLOW_REFRESH', True),

    'JWT_REFRESH_EXPIRATION_DELTA': env.timedelta(
        'JWT_REFRESH_EXPIRATION_DELTA',
        timedelta(days=7)),

    'JWT_ENCODE_HANDLER': env(
        'JWT_ENCODE_HANDLER',
        default='graphql_jwt.utils.jwt_encode'),

    'JWT_DECODE_HANDLER': env(
        'JWT_DECODE_HANDLER',
        default='graphql_jwt.utils.jwt_decode'),

    'JWT_PAYLOAD_HANDLER': env(
        'JWT_PAYLOAD_HANDLER',
        default='graphql_jwt.utils.jwt_payload'),
}

IMPORT_STRINGS = (
    'JWT_ENCODE_HANDLER',
    'JWT_DECODE_HANDLER',
    'JWT_PAYLOAD_HANDLER',
)


def perform_import(value, setting_name):
    if value is not None and isinstance(value, six.string_types):
        return import_from_string(value, setting_name)
    return value


def import_from_string(value, setting_name):
    try:
        module_path, class_name = value.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = 'Could not import `{}` for JWT setting `{}`. {}: {}.'.format(
            value, setting_name, e.__class__.__name__, e)
        raise ImportError(msg)


class JWTSettings(object):

    def __init__(self, defaults, import_strings):
        self.defaults = defaults
        self.import_strings = import_strings
        self._cached_attrs = set()

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError('Invalid setting: `{}`'.format(attr))

        value = self.user_settings.get(attr, self.defaults[attr])

        if attr in self.import_strings:
            value = perform_import(value, attr)

        self._cached_attrs.add(attr)
        setattr(self, attr, value)
        return value

    @property
    def user_settings(self):
        if not hasattr(self, '_user_settings'):
            self._user_settings = getattr(settings, 'GRAPHQL_JWT', {})
        return self._user_settings

    def reload(self):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()

        if hasattr(self, '_user_settings'):
            delattr(self, '_user_settings')


def reload_settings(*args, **kwargs):
    setting = kwargs['setting']

    if setting == 'GRAPHQL_JWT':
        jwt_settings.reload()


setting_changed.connect(reload_settings)

jwt_settings = JWTSettings(DEFAULTS, IMPORT_STRINGS)
