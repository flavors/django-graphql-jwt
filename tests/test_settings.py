from datetime import timedelta

from django.test import TestCase

from graphql_jwt import settings


class SettingsTests(TestCase):
    def test_perform_import(self):
        f = settings.perform_import(id, "")
        self.assertEqual(f, id)

        f = settings.perform_import("datetime.timedelta", "")
        self.assertEqual(f, timedelta)

    def test_import_from_string_error(self):
        with self.assertRaises(ImportError):
            settings.import_from_string("import.error", "")

    def test_reload_settings(self):
        getattr(settings.jwt_settings, "JWT_ALGORITHM")
        settings.reload_settings(setting="TEST")

        self.assertTrue(settings.jwt_settings._cached_attrs)

        delattr(settings.jwt_settings, "_user_settings")
        settings.jwt_settings.reload()

        self.assertFalse(settings.jwt_settings._cached_attrs)
