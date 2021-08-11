<p align="center">
  <a href="https://django-graphql-jwt.domake.io/"><img width="420px" src="https://django-graphql-jwt.domake.io/_static/logo.png" alt='Django GraphQL JWT'></a>
</p>

<p align="center">
    JSON Web Token authentication for Django GraphQL.
    <br>Fantastic <strong>documentation</strong> is available at <a href="https://django-graphql-jwt.domake.io">https://django-graphql-jwt.domake.io</a>.
</p>
<p align="center">
    <a href="https://github.com/flavors/django-graphql-jwt/actions">
        <img src="https://github.com/flavors/django-graphql-jwt/actions/workflows/test-suite.yml/badge.svg" alt="Test">
    </a>
    <a href="https://codecov.io/gh/flavors/django-graphql-jwt">
        <img src="https://img.shields.io/codecov/c/github/flavors/django-graphql-jwt?color=%2334D058" alt="Coverage">
    </a>
    <a href="https://www.codacy.com/gh/flavors/django-graphql-jwt/dashboard">
        <img src="https://app.codacy.com/project/badge/Grade/4f9fd439fbc74be88a215b9ed2abfcf9" alt="Codacy">
    </a>
    <a href="https://pypi.python.org/pypi/django-graphql-jwt">
        <img src="https://img.shields.io/pypi/v/django-graphql-jwt.svg" alt="Package version">
    </a>
</p>

## Installation

Install last stable version from Pypi:

```sh
pip install django-graphql-jwt
```

Add `AuthenticationMiddleware` middleware to your *MIDDLEWARE* settings:


```py
MIDDLEWARE = [
    # ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    # ...
]
```

Add `JSONWebTokenMiddleware` middleware to your *GRAPHENE* settings:

```py
GRAPHENE = {
    "SCHEMA": "mysite.myschema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}
```

Add `JSONWebTokenBackend` backend to your *AUTHENTICATION_BACKENDS*:

```py
AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]
```

## Schema

Add *django-graphql-jwt* mutations to the root schema:

```py
import graphene
import graphql_jwt


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation)
```
