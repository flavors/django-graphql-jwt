INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test',
    },
}

SECRET_KEY = 'test'

GRAPHENE = {
    'SCHEMA': 'tests.schema.schema',
}

AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JWTBackend',
]

ROOT_URLCONF = 'tests.urls'
