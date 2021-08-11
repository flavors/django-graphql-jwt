Changelog
=========

0.3.4
-----

* Added JSONWebTokenBackend.get_user method

0.3.3
-----

* Added Graphene V2 support

0.3.2
-----

* Added support for PyJWT>=2
* Removed signals providing_args
* Added JWT_COOKIE_SAMESITE setting
* Added support for Graphene v3

0.3.1
-----

* Set JWT-refresh-token cookie on tokenAuth mutation
* Read token/refresh-token from cookies (TokenAuth, Refresh, Verify and Revoke mutations)
* Add refreshExpiresIn field
* Add token payload to tokenAuth mutation
* Add DeleteJSONWebTokenCookie and DeleteRefreshTokenCookie mutations
* Add JWT_REUSE_REFRESH_TOKENS setting in order to reuse the refresh token instances
* Add JWT_HIDE_TOKEN_FIELDS setting (prevent XSS exploitation)
* Add JWT_CSRF_ROTATION setting
* Add JWT_COOKIE_PATH and JWT_COOKIE_DOMAIN settings
* Removed ugettext in favor of gettext

0.3.0
-----

* Added Django 3.0 support
* Removed Python 2.7 support

0.2.3
-----

* Fixed refresh_token cookie
* Added middleware method to SchemaRequestFactory
* Added arabic, french and portuguese translations

0.2.2
-----

* Removed DjangoMiddleware
* Added dutch and french locales
* Added JWT Refresh token cookie
* Added signals
* Added JWT_GET_USER_BY_NATURAL_KEY_HANDLER

0.2.1
-----

* Added JWT cookie authentication
* Added refresh_token_lazy
* Fixed RefreshToken related name
* WARNING: Added kwargs argument to JSONWebTokenMutation.resolve()
* Fixed @context decorator to determine the info argument
* Added _cached_token to refresh token instances to allow hashed tokens
* Added JWT_GET_REFRESH_TOKEN_HANDLER setting variable
* Improved argument authentication using multiple credentials
* Added execute method to SchemaTestCase
* Added graphql_jwt classes to JWT_ALLOW_ANY_CLASSES
* Added @superuser_required decorator

0.2.0
-----

* Added Graphene middleware
* Added JWT_ALLOW_ANY_HANDLER setting
* Added Per-argument authentication
* Added JSONWebTokenExpired exception
* Included Sphinx documentation
* Renamed JWT_AUTH_HEADER to JWT_AUTH_HEADER_NAME

0.1.14
------

* Added long running refresh tokens
* Renamed orig_iat to origIat
* Added request argument to get_user_by_token

0.1.13
------

* Added unittest subclasses for writing tests
* Renamed GraphQLJWTError to JSONWebTokenError

0.1.12
------

* Fixed context.META attribute

0.1.11
------

* Removed environment settings variables
* Added JWT_AUTH_HEADER setting
* Added JWT_PAYLOAD_GET_USERNAME_HANDLER setting
* Fixed TokenAuth mutation when user is already authenticated

0.1.10
------

* Added JWTSettings
* Added jwt-handlers to settings
* Added context argument to jwt-handlers

0.1.9
-----

* Included auth decorators

0.1.8
-----

* Added old style middleware support

0.1.7
-----

* Added anonymous-hyperlink

0.1.6
-----

* Added Python 2.7 support

0.1.5
-----

* Removed login() usage
* Renamed do_auth() to resolve()

0.1.4
-----

* Renamed JWTMiddleware to JSONWebTokenMiddleware
* Renamed JWTBackend to JSONWebTokenBackend
* ObtainJSONWebToken mutation
* Customizing, JSONWebTokenMutation abstract class

0.1.3
-----

* Complete support for Relay

0.1.2
-----

* Shortcuts, get_token
* Modified Refresh output fields
* Updated README, don’t include the token as a UserType field

0.1.1
-----

* Fixed rst paragraphs blocks

0.1.0
-----

* Fixed 'es' locale directory
* Removed JWT_VERIFY_REFRESH_EXPIRATION
* JWT_LEEWAY timedelta type
* 100% coverage
* A pretty README
* Support Python 3.7

0.0.2
-----

* Fixed auth backend missing token

0.0.1
-----

* xin chào!
