Django GraphQL JWT
==================

|Pypi| |Wheel| |Build Status| |Codecov| |Code Climate|


`JSON Web Token`_ authentication for `Django GraphQL`_

.. _JSON Web Token: https://jwt.io/
.. _Django GraphQL: https://github.com/graphql-python/graphene-django


Dependencies
------------

* Django ≥ 1.11


Installation
------------

Install last stable version from Pypi.

.. code:: sh

    pip install django-graphql-jwt


Include the ``JSONWebTokenMiddleware`` middleware in your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ...
    ]

Include the ``JSONWebTokenBackend`` backend in your *AUTHENTICATION_BACKENDS* settings:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JSONWebTokenBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]


Schema
------

Add mutations to the root schema.

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()

    schema = graphene.Schema(mutations=Mutations)


- ``tokenAuth`` to authenticate the user and obtain the JSON Web Token.

The mutation uses your User's model `USERNAME_FIELD`_, which by default is ``username``.

.. _USERNAME_FIELD: https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.CustomUser

.. code:: graphql

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
      }
    }


- ``verifyToken`` to confirm that the *token* is valid.

.. code:: graphql

    mutation VerifyToken($token: String!) {
      verifyToken(token: $token) {
        payload
      }
    }


- ``refreshToken`` to obtain a brand new *token* with renewed expiration time for **non-expired tokens**.

`[wiki] <https://github.com/flavors/django-graphql-jwt/wiki/Token-expiration>`_ Configure your *refresh token* scenario and set the flag ``JWT_VERIFY_EXPIRATION=true``.


.. code:: graphql

    mutation RefreshToken($token: String!) {
      refreshToken(token: $token) {
        token
        payload
      }
    }


Authentication in GraphQL queries
---------------------------------

Now in order to access protected API you must include the ``Authorization: JWT <token>`` header.

Django-graphql-jwt uses middleware to hook the authenticated user into request object. The simple, raw way to limit access to data is to check ``info.context.user.is_authenticated``:

.. code:: python

    import graphene


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)

        def resolve_viewer(self, info, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise Exception('Authentication credentials were not provided')
            return user


`[wiki] <https://github.com/flavors/django-graphql-jwt/wiki/Auth-decorators>`_ As a shortcut, you can use a ``login_required()`` decorator for your queries and mutations:

.. code:: python

    import graphene


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)

        @login_required
        def resolve_viewer(self, info, **kwargs):
            return info.context.user


Relay
-----

Complete support for `Relay`_.

.. _Relay: https://facebook.github.io/relay/

.. code:: python

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.relay.Verify.Field()
        refresh_token = graphql_jwt.relay.Refresh.Field()


Customizing
-----------

If you want to customize the ``ObtainJSONWebToken`` behavior, you'll need to customize the ``.resolve()`` method on a subclass of ``JSONWebTokenMutation`` or ``.relay.JSONWebTokenMutation``.

.. code:: python

    import graphene
    import graphql_jwt


    class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
        user = graphene.Field(UserType)

        @classmethod
        def resolve(cls, root, info):
            return cls(user=info.context.user)

Authenticate the user and obtain the *token* and the *user id*.

.. code:: graphql

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        user {
          id
        }
      }
    }


Environment variables
---------------------

`JWT_ALGORITHM`_

::

    Algorithm for cryptographic signing
    Default: HS256 

`JWT_AUDIENCE`_

::

    Identifies the recipients that the JWT is intended for
    Default: None

`JWT_ISSUER`_

::

    Identifies the principal that issued the JWT
    Default: None

`JWT_LEEWAY`_

::

    Validate an expiration time which is in the past but not very far
    Default: seconds=0

`JWT_SECRET_KEY`_

::

    The secret key used to sign the JWT
    Default: settings.SECRET_KEY

`JWT_VERIFY`_

::

    Secret key verification
    Default: True

`JWT_VERIFY_EXPIRATION`_

::

    Expiration time verification
    Default: False

JWT_EXPIRATION_DELTA

::

    Timedelta added to utcnow() to set the expiration time
    Default: minutes=5

JWT_ALLOW_REFRESH

::

    Enable token refresh
    Default: True

JWT_REFRESH_EXPIRATION_DELTA

::

    Limit on token refresh
    Default: days=7

JWT_AUTH_HEADER_PREFIX

::

    Authorization prefix
    Default: JWT


.. _JWT_ALGORITHM: https://pyjwt.readthedocs.io/en/latest/algorithms.html
.. _JWT_AUDIENCE: http://pyjwt.readthedocs.io/en/latest/usage.html#audience-claim-aud
.. _JWT_ISSUER: http://pyjwt.readthedocs.io/en/latest/usage.html#issuer-claim-iss
.. _JWT_LEEWAY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=leeway#expiration-time-claim-exp
.. _JWT_SECRET_KEY: http://pyjwt.readthedocs.io/en/latest/algorithms.html?highlight=secret+key#asymmetric-public-key-algorithms
.. _JWT_VERIFY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify#reading-the-claimset-without-validation
.. _JWT_VERIFY_EXPIRATION: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify_exp#expiration-time-claim-exp

----

Credits to `@jpadilla`_ / `django-rest-framework-jwt`_.

.. _@jpadilla: https://github.com/jpadilla
.. _django-rest-framework-jwt: https://github.com/GetBlimp/django-rest-framework-jwt


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Wheel| image:: https://img.shields.io/pypi/wheel/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-jwt.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-jwt

.. |Codecov| image:: https://img.shields.io/codecov/c/github/flavors/django-graphql-jwt.svg
   :target: https://codecov.io/gh/flavors/django-graphql-jwt

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/c79a185d546f7e34fdd6/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-jwt
