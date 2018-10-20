from contextlib import contextmanager
from datetime import datetime, timedelta

from graphql_jwt.settings import jwt_settings

from .compat import mock


@contextmanager
def catch_signal(signal):
    handler = mock.Mock()
    signal.connect(handler)
    yield handler
    signal.disconnect(handler)


@contextmanager
def back_to_the_future(**kwargs):
    with mock.patch('graphql_jwt.utils.datetime') as datetime_mock:
        datetime_mock.utcnow.return_value =\
            datetime.utcnow() + timedelta(**kwargs)
        yield datetime_mock


def refresh_expired():
    expires = jwt_settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()
    return back_to_the_future(seconds=1 + expires)
