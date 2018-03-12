from django.test.utils import TestContextDecorator

from graphql_jwt import settings


class override_settings(TestContextDecorator):

    def __init__(self, **kwargs):
        self.options = kwargs
        self.overridden_settings = {}
        super(override_settings, self).__init__()

    def enable(self):
        for key, new_value in self.options.items():
            self.overridden_settings[key] = getattr(settings, key)
            setattr(settings, key, new_value)

    def disable(self):
        for key in self.options:
            setattr(settings, key, self.overridden_settings[key])
