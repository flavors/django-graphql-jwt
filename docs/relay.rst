Relay
=====

Complete support for `Relay <https://facebook.github.io/relay/>`_.

Schema
-------
Add mutations to the root schema::

    import graphene
    import graphql_jwt


    class Mutations(graphene.ObjectType):
        token_auth = graphql_jwt.relay.ObtainJSONWebToken.Field()
        verify_token = graphql_jwt.relay.Verify.Field()
        refresh_token = graphql_jwt.relay.Refresh.Field()

        # Long running refresh tokens
        revoke_token = graphql_jwt.relay.Revoke.Field()


    schema = graphene.Schema(mutation=Mutations)


Queries
-------

Relay mutations only accepts one argument named *input*.


* ``tokenAuth`` to authenticate the user and obtain the **JSON Web Token**:

  ::

      mutation TokenAuth($username: String!, $password: String!) {
        tokenAuth(input: {username: $username, password: $password}) {
          token
        }
      }

* ``verifyToken`` to validate the *token* and obtain the *token payload*:

  ::

      mutation VerifyToken($token: String!) {
        verifyToken(input: {token: $token}) {
          payload
        }
      }


Single token refresh
~~~~~~~~~~~~~~~~~~~~

* ``refreshToken`` to obtain a brand new *token* with renewed expiration time for **non-expired tokens**:

  ::

      mutation RefreshToken($token: String!) {
        refreshToken(input: {token: $token}) {
          token
          payload
        }
      }


Long running refresh tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``refreshToken`` to refresh your *token*, using the ``refreshToken`` you already got during authorization:

  ::

      mutation RefreshToken($refreshToken: String!) {
        refreshToken(input: {refreshToken: $refreshToken}) {
          token
          refreshToken
          payload
        }
      }

* ``revokeToken`` to revoke a valid ``refreshToken``. The invalidation takes place immediately, and the ``refreshToken`` cannot be used again after the revocation:

  ::

      mutation RevokeToken($refreshToken: String!) {
        revokeToken(input: {refreshToken: $refreshToken}) {
          revoked
        }
      }


Customizing
-----------

If you want to customize the ``ObtainJSONWebToken`` behavior, you'll need to customize the ``resolve()`` method on a subclass of:

  .. autoclass:: graphql_jwt.relay.JSONWebTokenMutation

::

    import graphene
    import graphql_jwt


    class ObtainJSONWebToken(graphql_jwt.relay.JSONWebTokenMutation):
        user = graphene.Field(UserType)

        @classmethod
        def resolve(cls, root, info):
            return cls(user=info.context.user)

Authenticate the user and obtain the **JSON Web Token** and the *user id*::

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(input: {username: $username, password: $password}) {
        token
        user {
          id
        }
      }
    }
