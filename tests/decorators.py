import contextlib

from graphql_jwt import settings


@contextlib.contextmanager
def override_settings(**override):
    restore = {}

    try:
        for var, value in override.items():
            restore[var] = getattr(settings, var)
            setattr(settings, var, value)
        yield
    finally:
        for var, value in restore.items():
            setattr(settings, var, value)
