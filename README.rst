Django GraphQL JWT
==================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


JSON Web Token for GraphQL

Dependencies
------------

* Python ≥ 3.4
* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-jwt


Include the JWT middleware in your `MIDDLEWARE` settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'graphql_jwt.middleware.JWTMiddleware',
        ...
    ]

Include the JWT backend in your `AUTHENTICATION_BACKENDS` settings:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JWTBackend',
        'django.contrib.auth.backends.ModelBackend'
    ]

Token mutations
---------------

Add mutations to your GraphQL schema

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()

    schema = graphene.Schema(mutations=Mutations)


User Node
---------

Let's start by creating a simple `UserNode`

.. code:: python

    import graphene

    from django.contrib.auth import get_user_model
    from graphene_django import DjangoObjectType

    from graphql_jwt.utils import jwt_encode, jwt_payload


    class UserNode(DjangoObjectType):
        token = graphene.String()

        class Meta:
            model = get_user_model()

        def resolve_token(self, info, **kwargs):
            if info.context.user != self:
                return None

            payload = jwt_payload(self)
            return jwt_encode(payload)

Login mutation
--------------

.. code:: python

    import graphene

    from django.contrib.auth import authenticate, login

    class LogIn(graphene.Mutation):
        user = graphene.Field(UserNode)

        class Arguments:
            username = graphene.String()
            password = graphene.String()

        @classmethod
        def mutate(cls, root, info, username, password):
            user = authenticate(username=username, password=password)

            if user is not None:
                raise Exception('Please enter a correct phone and password')

            if not user.is_active:
                raise Exception('It seems your account has been disabled')

            login(info.context, user)
            return cls(user=user)


Environment variables
---------------------

- JWT_ALGORITHM
- JWT_AUDIENCE
- JWT_AUTH_HEADER_PREFIX
- JWT_ISSUER
- JWT_LEEWAY
- JWT_SECRET_KEY
- JWT_VERIFY
- JWT_VERIFY_EXPIRATION
- JWT_EXPIRATION_DELTA
- JWT_ALLOW_REFRESH
- JWT_VERIFY_REFRESH_EXPIRATION
- JWT_REFRESH_EXPIRATION_DELTA


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Build Status| image:: https://travis-ci.org/flavors/graphql-jwt.svg?branch=master
   :target: https://travis-ci.org/flavors/graphql-jwt

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/graphql-jwt.svg
   :target: https://codecov.io/gh/flavors/graphql-jwt

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/7ca6c7ced3df021b7915/maintainability
   :target: https://codeclimate.com/github/flavors/graphql-jwt
