from django.test import override_settings


class override_jwt_settings(override_settings):

    def __init__(self, **kwargs):
        super().__init__(GRAPHQL_JWT=kwargs)
