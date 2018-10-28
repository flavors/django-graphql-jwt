Customizing
===========

If you want to customize the ``ObtainJSONWebToken`` behavior, you'll need to customize the ``resolve()`` method on a subclass of:

  .. autoclass:: graphql_jwt.JSONWebTokenMutation

::

    import graphene
    import graphql_jwt


    class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
        user = graphene.Field(UserType)

        @classmethod
        def resolve(cls, root, info):
            return cls(user=info.context.user)

Authenticate the user and obtain a **JSON Web Token** and the *user id*::

    mutation TokenAuth($username: String!, $password: String!) {
      tokenAuth(username: $username, password: $password) {
        token
        user {
          id
        }
      }
    }
