import datetime
import environ

from django.conf import settings

env = environ.Env()


def timedelta(name, **defaults):
    args = env.dict(name, default={})

    if args:
        args = {k: int(v) for k, v in args.items()}
    else:
        args = defaults
    return datetime.timedelta(**args)


JWT_ALGORITHM = env('JWT_ALGORITHM', default='HS256')
JWT_AUDIENCE = env('JWT_AUDIENCE', default=None)
JWT_AUTH_HEADER_PREFIX = env('JWT_AUTH_HEADER_PREFIX', default='JWT')
JWT_ISSUER = env('JWT_ISSUER', default=None)
JWT_LEEWAY = env.int('JWT_LEEWAY', 0)
JWT_SECRET_KEY = env('JWT_SECRET_KEY', default=settings.SECRET_KEY)

JWT_VERIFY = env.bool('JWT_VERIFY', True)
JWT_VERIFY_EXPIRATION = env.bool('JWT_VERIFY_EXPIRATION', False)
JWT_EXPIRATION_DELTA = timedelta('JWT_EXPIRATION_DELTA', seconds=60 * 5)

JWT_ALLOW_REFRESH = env.bool('JWT_ALLOW_REFRESH', True)
JWT_VERIFY_REFRESH_EXPIRATION =\
    env.bool('JWT_VERIFY_REFRESH_EXPIRATION', True)

JWT_REFRESH_EXPIRATION_DELTA =\
    timedelta('JWT_REFRESH_EXPIRATION_DELTA', days=7)
