INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'graphql_jwt.refresh_token',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'test'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'graphql_jwt.backends.JSONWebTokenBackend',
]
