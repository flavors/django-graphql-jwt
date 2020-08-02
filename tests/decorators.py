import django
from django.test import override_settings

import pytest


class override_jwt_settings(override_settings):

    def __init__(self, **kwargs):
        super().__init__(GRAPHQL_JWT=kwargs)


def skipif_django_version(version):
    return pytest.mark.skipif(
        django.get_version() < version,
        reason=f'Django < {version} is not supported')
