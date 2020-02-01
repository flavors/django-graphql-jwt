Signals
=======

*django-graphql-jwt* uses the following signals:

token_issued
------------

Sent when a user authenticates successfully.

Arguments sent with this signal:
    - sender: The class of the Graphene's mutation.
    - request: The current HttpRequest instance.
    - user: The user instance that just authenticated.


token_refreshed
---------------

Sent when a single token has been refreshed.

Arguments sent with this signal:
    - sender: The class of the Graphene's mutation.
    - request: The current HttpRequest instance.
    - user: The user instance that just refreshed a single token.


refresh_token_rotated
---------------------

Sent when a long running refresh token has been rotated.

Arguments sent with this signal:
    - sender: The class of the refresh_token that just rotated.
    - request: The current HttpRequest instance.
    - refresh_token: The RefreshToken instance that just rotated.
    - old_token: The refresh token used to refresh.


refresh_token_revoked
---------------------

Sent when a long running refresh token has been revoked.

Arguments sent with this signal:
    - sender: The class of the refresh_token that just revoked.
    - request: The current HttpRequest instance.
    - refresh_token: The RefreshToken instance that just revoked.
