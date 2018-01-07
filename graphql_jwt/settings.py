from datetime import timedelta

from django.conf import settings

import environ


class Env(environ.Env):

    def timedelta(self, var, default=environ.Env.NOTSET):

        def cast(value):
            args = [val.split('=') for val in value.split(',') if val]
            return timedelta(**{name: float(val) for name, val in args})

        return self.get_value(var, cast=cast, default=default)


env = Env()

JWT_ALGORITHM = env('JWT_ALGORITHM', default='HS256')
JWT_AUDIENCE = env('JWT_AUDIENCE', default=None)
JWT_AUTH_HEADER_PREFIX = env('JWT_AUTH_HEADER_PREFIX', default='JWT')
JWT_ISSUER = env('JWT_ISSUER', default=None)
JWT_LEEWAY = env.timedelta('JWT_LEEWAY', 0)
JWT_SECRET_KEY = env('JWT_SECRET_KEY', default=settings.SECRET_KEY)

JWT_VERIFY = env.bool('JWT_VERIFY', True)
JWT_VERIFY_EXPIRATION = env.bool('JWT_VERIFY_EXPIRATION', False)

JWT_EXPIRATION_DELTA = env.timedelta(
    'JWT_EXPIRATION_DELTA',
    timedelta(seconds=60 * 5),
)

JWT_ALLOW_REFRESH = env.bool('JWT_ALLOW_REFRESH', True)
JWT_REFRESH_EXPIRATION_DELTA = env.timedelta(
    'JWT_REFRESH_EXPIRATION_DELTA',
    timedelta(days=7),
)
