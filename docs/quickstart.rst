Quickstart
==========

Dependencies
------------

* Django ≥ 1.11


Installation
------------

Install last stable version v\ |version| from Pypi::

    pip install django-graphql-jwt

Add ``AuthenticationMiddleware`` middleware to your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
    ]

Add ``JSONWebTokenMiddleware`` middleware to your *GRAPHENE* settings::

    GRAPHENE = {
        'SCHEMA': 'mysite.myschema.schema',
        'MIDDLEWARE': [
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ],
    }

Add ``JSONWebTokenBackend`` backend to your *AUTHENTICATION_BACKENDS*::

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JSONWebTokenBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]


Schema
------

Add mutations to the root schema::

    import graphene
    import graphql_jwt


    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()


    schema = graphene.Schema(mutation=Mutation)


Queries
-------

* ``tokenAuth`` to authenticate the user and obtain a **JSON Web Token**.

  The mutation uses your User's model `USERNAME_FIELD <https://docs.djangoproject.com/en/2.0/topics/auth/customizing/#django.contrib.auth.models.CustomUser>`_, which by default is ``username``:

  ::

      mutation TokenAuth($username: String!, $password: String!) {
        tokenAuth(username: $username, password: $password) {
          token
        }
      }


* ``verifyToken`` to validate the *token* and obtain the *token payload*:

  ::

      mutation VerifyToken($token: String!) {
        verifyToken(token: $token) {
          payload
        }
      }


* ``refreshToken`` to obtain a brand new *token* with renewed expiration time for **non-expired tokens**:

  :doc:`Configure your refresh token <refresh_token>` scenario and set to ``True`` the :doc:`JWT_VERIFY_EXPIRATION<settings>` setting.
