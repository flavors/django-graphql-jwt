from functools import wraps

import django
from django.test import override_settings

import pytest


class override_jwt_settings(override_settings):

    def __init__(self, **kwargs):
        super(override_jwt_settings, self).__init__(GRAPHQL_JWT=kwargs)


def skipif_django_version(version):
    return pytest.mark.skipif(
        django.get_version() < version,
        reason='Django < {} is not supported'.format(version))


def input_variables(f):
    @wraps(f)
    def wrapper(self, variables):
        return f(self, {'input': variables})
    return wrapper
