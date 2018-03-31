from django.test import override_settings


class override_jwt_settings(override_settings):

    def __init__(self, **kwargs):
        super(override_jwt_settings, self).__init__(GRAPHQL_JWT=kwargs)
