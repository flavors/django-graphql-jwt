INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

SECRET_KEY = 'test'

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JWTBackend',
]
