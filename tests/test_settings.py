from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase

from graphql_jwt import settings


class SettingsTests(TestCase):

    @patch.dict('os.environ', {
        'TEST_TIMEDELTA': 'hours=1,days=1'
    })
    def test_env_timedelta_cast(self):
        env = settings.Env()
        var = env.timedelta('TEST_TIMEDELTA')

        self.assertEqual(var, timedelta(hours=1, days=1))
