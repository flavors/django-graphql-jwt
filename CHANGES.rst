Changelog
=========

0.2.0
-----

* Added Graphene middleware
* Added JSONWebTokenExpired exception
* Added documentation
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
