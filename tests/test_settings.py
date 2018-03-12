from datetime import timedelta

from django.test import TestCase

from graphql_jwt import settings

from .compat import mock


class SettingsTests(TestCase):

    @mock.patch.dict('os.environ', {
        'TEST_TIMEDELTA': 'hours=1,days=1',
    })
    def test_env_timedelta_cast(self):
        env = settings.Env()
        var = env.timedelta('TEST_TIMEDELTA')

        self.assertEqual(var, timedelta(hours=1, days=1))
