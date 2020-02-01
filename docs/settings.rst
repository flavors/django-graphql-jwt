Settings
========

*Django-graphql-jwt* reads your configuration from a single **Django setting** named ``GRAPHQL_JWT``::

    GRAPHQL_JWT = {
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_EXPIRATION_DELTA': timedelta(minutes=10),
    }


Here's a **list of settings** available in *django-graphql-jwt* and their default values:


PyJWT
-----

`JWT_ALGORITHM`_
~~~~~~~~~~~~~~~~

  Algorithm for cryptographic signing

  Default: ``'HS256'``


`JWT_AUDIENCE`_
~~~~~~~~~~~~~~~

  Identifies the recipients that the JWT is intended for

  Default: ``None``


`JWT_ISSUER`_
~~~~~~~~~~~~~

  Identifies the principal that issued the JWT

  Default: ``None``


`JWT_LEEWAY`_
~~~~~~~~~~~~~

  Validate an expiration time which is in the past but not very far

  Default: ``timedelta(seconds=0)``


`JWT_SECRET_KEY`_
~~~~~~~~~~~~~~~~~

  The secret key used to sign the JWT

  Default: ``settings.SECRET_KEY``


`JWT_VERIFY`_
~~~~~~~~~~~~~

  Secret key verification

  Default: ``True``


JWT_ENCODE_HANDLER
~~~~~~~~~~~~~~~~~~

  A custom function to encode the token

  .. autofunction:: graphql_jwt.utils.jwt_encode


JWT_DECODE_HANDLER
~~~~~~~~~~~~~~~~~~

  A custom function to decode the token

  .. autofunction:: graphql_jwt.utils.jwt_decode


JWT_PAYLOAD_HANDLER
~~~~~~~~~~~~~~~~~~~

  A custom function to generate the token payload

  .. autofunction:: graphql_jwt.utils.jwt_payload


JWT_PAYLOAD_GET_USERNAME_HANDLER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  A custom function to obtain the username::

    lambda payload: payload.get(get_user_model().USERNAME_FIELD)


JWT_GET_USER_BY_NATURAL_KEY_HANDLER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  A custom function to get User object from username

  .. autofunction:: graphql_jwt.utils.get_user_by_natural_key


Token expiration
----------------

`JWT_VERIFY_EXPIRATION`_
~~~~~~~~~~~~~~~~~~~~~~~~

  Expiration time verification

  Default: ``False``


JWT_EXPIRATION_DELTA
~~~~~~~~~~~~~~~~~~~~

  Timedelta added to *utcnow()* to set the expiration time

  Default: ``timedelta(minutes=5)``


Refresh token
-------------

JWT_ALLOW_REFRESH
~~~~~~~~~~~~~~~~~

  Enable token refresh

  Default: ``True``


JWT_REFRESH_EXPIRATION_DELTA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Limit on token refresh

  Default: ``timedelta(days=7)``


JWT_LONG_RUNNING_REFRESH_TOKEN
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  Enable long time running refresh token

  Default: ``False``


JWT_REFRESH_TOKEN_MODEL
~~~~~~~~~~~~~~~~~~~~~~~

  The model to use to represent a refresh token

  .. autoclass:: graphql_jwt.refresh_token.models.RefreshToken


JWT_REFRESH_TOKEN_N_BYTES
~~~~~~~~~~~~~~~~~~~~~~~~~

  Long running refresh token number of bytes

  Default: ``20``


JWT_REUSE_REFRESH_TOKENS
~~~~~~~~~~~~~~~~~~~~~~~~

  Reuse the long running refreshed token instead of generating a new one

  Default: ``False``


JWT_REFRESH_EXPIRED_HANDLER
~~~~~~~~~~~~~~~~~~~~~~~~~~~

  A custom function to determine if refresh has expired

  .. autofunction:: graphql_jwt.utils.refresh_has_expired


JWT_GET_REFRESH_TOKEN_HANDLER
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  A custom function to retrieve a long time refresh token instance

  .. autofunction:: graphql_jwt.refresh_token.utils.get_refresh_token_by_model


Permissions
-----------

JWT_ALLOW_ANY_HANDLER
~~~~~~~~~~~~~~~~~~~~~

    A custom function to determine the non-authentication **per-field**

    .. autofunction:: graphql_jwt.middleware.allow_any


JWT_ALLOW_ANY_CLASSES
~~~~~~~~~~~~~~~~~~~~~

  A list or tuple of Graphene classes that do not need authentication
  
  Default: ``()``


HTTP header
-----------

JWT_AUTH_HEADER_NAME
~~~~~~~~~~~~~~~~~~~~

  Authorization header name

  Default: ``'HTTP_AUTHORIZATION'``


JWT_AUTH_HEADER_PREFIX
~~~~~~~~~~~~~~~~~~~~~~

  Authorization header prefix

  Default: ``'JWT'``


Per-argument
------------

JWT_ALLOW_ARGUMENT
~~~~~~~~~~~~~~~~~~

  Allow per-argument authentication system

  Default: ``False``


JWT_ARGUMENT_NAME
~~~~~~~~~~~~~~~~~

  Argument name for per-argument authentication system

  Default: ``'token'``


Cookie authentication
---------------------

JWT_COOKIE_NAME
~~~~~~~~~~~~~~~

  The name of the cookie when HTTP cookies are used as a valid transport for the token

  Default: ``'JWT'``

JWT_REFRESH_TOKEN_COOKIE_NAME
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

  The name of the cookie when HTTP cookies are used as a valid transport for the refresh token

  Default: ``'JWT-refresh-token'``


JWT_COOKIE_SECURE
~~~~~~~~~~~~~~~~~

  Whether to use a secure cookie for the JWT cookie. If this is set to True, the cookie will be marked as "secure", which means browsers may ensure that the cookie is only sent under an HTTPS connection.

  Default: ``False``


.. _JWT_ALGORITHM: https://pyjwt.readthedocs.io/en/latest/algorithms.html
.. _JWT_AUDIENCE: http://pyjwt.readthedocs.io/en/latest/usage.html#audience-claim-aud
.. _JWT_ISSUER: http://pyjwt.readthedocs.io/en/latest/usage.html#issuer-claim-iss
.. _JWT_LEEWAY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=leeway#expiration-time-claim-exp
.. _JWT_SECRET_KEY: https://pyjwt.readthedocs.io/en/latest/usage.html?highlight=secret%20key#usage-examples
.. _JWT_VERIFY: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify#reading-the-claimset-without-validation
.. _JWT_VERIFY_EXPIRATION: http://pyjwt.readthedocs.io/en/latest/usage.html?highlight=verify_exp#expiration-time-claim-exp
