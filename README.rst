Django GraphQL JWT
==================

.. image:: https://api.codacy.com/project/badge/Grade/4f9fd439fbc74be88a215b9ed2abfcf9
   :alt: Codacy Badge
   :target: https://app.codacy.com/gh/flavors/django-graphql-jwt?utm_source=github.com&utm_medium=referral&utm_content=flavors/django-graphql-jwt&utm_campaign=Badge_Grade_Dashboard

|Pypi| |Build Status| |Codecov| |Code Climate|


`JSON Web Token <https://jwt.io/>`_ authentication for `Django GraphQL <https://github.com/graphql-python/graphene-django>`_


Installation
------------

Install last stable version from Pypi:

::

    pip install django-graphql-jwt

Add ``AuthenticationMiddleware`` middleware to your *MIDDLEWARE* settings:

.. code:: python

    MIDDLEWARE = [
        ...
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        ...
    ]

Add ``JSONWebTokenMiddleware`` middleware to your *GRAPHENE* settings:

.. code:: python

    GRAPHENE = {
        'SCHEMA': 'mysite.myschema.schema',
        'MIDDLEWARE': [
            'graphql_jwt.middleware.JSONWebTokenMiddleware',
        ],
    }

Add ``JSONWebTokenBackend`` backend to your *AUTHENTICATION_BACKENDS*:

.. code:: python

    AUTHENTICATION_BACKENDS = [
        'graphql_jwt.backends.JSONWebTokenBackend',
        'django.contrib.auth.backends.ModelBackend',
    ]


Schema
------

Add *django-graphql-jwt* mutations to the root schema:

.. code:: python

    import graphene
    import graphql_jwt


    class Mutation(graphene.ObjectType):
        token_auth = graphql_jwt.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.Verify.Field()
        refresh_token = graphql_jwt.Refresh.Field()


    schema = graphene.Schema(mutation=Mutation)


Documentation
-------------

Fantastic documentation is available at https://django-graphql-jwt.domake.io.


.. |Pypi| image:: https://img.shields.io/pypi/v/django-graphql-jwt.svg
   :target: https://pypi.python.org/pypi/django-graphql-jwt
   :alt: Pypi

.. |Build Status| image:: https://travis-ci.org/flavors/django-graphql-jwt.svg?branch=master
   :target: https://travis-ci.org/flavors/django-graphql-jwt
   :alt: Build Status

.. |Codecov| image:: https://codecov.io/gh/flavors/django-graphql-jwt/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/flavors/django-graphql-jwt
   :alt: Codecov

.. |Code Climate| image:: https://api.codeclimate.com/v1/badges/c79a185d546f7e34fdd6/maintainability
   :target: https://codeclimate.com/github/flavors/django-graphql-jwt
   :alt: Codeclimate
