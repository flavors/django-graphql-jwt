Authentication
==============

*Django-graphql-jwt* uses a `Graphene middleware <https://docs.graphene-python.org/en/latest/execution/middleware/>`_ to hook the authenticated user into *context* object. The simple, raw way to limit access to data is to check ``info.context.user.is_authenticated``::

    import graphene


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)

        def resolve_viewer(self, info, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Authentication credentials were not provided")
            return user


As a shortcut, you can use :doc:`decorators<decorators>` for your *resolvers* and *mutations*.


HTTP header
-----------

Now in order to access protected API you must include the ``Authorization`` HTTP header:

.. code-block:: http

    POST / HTTP/1.1
    Host: domake.io
    Authorization: JWT <token>
    Content-Type: application/json;


Per-cookie
----------

When a token is requested and ``jwt_cookie`` decorator is set, the response will set the given cookie with the token string::

    from django.urls import path

    from graphene_django.views import GraphQLView
    from graphql_jwt.decorators import jwt_cookie

    urlpatterns = [
        path("graphql/", jwt_cookie(GraphQLView.as_view())),
    ]


If the ``jwt_cookie`` decorator is set, consider adding `CSRF middleware <https://docs.djangoproject.com/es/2.1/ref/csrf/>`_ ``"django.middleware.csrf.CsrfViewMiddleware"`` to provide protection against `Cross Site Request Forgeries <https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)>`_.

A cookie-based authentication does not require sending the tokens as a mutation input argument.

Delete Cookies
~~~~~~~~~~~~~~

In order to prevent XSS (cross-site scripting) attacks, cookies have the ``HttpOnly`` flag set, so you cannot delete them on the client-side. This package includes some mutations to delete the cookies on the server-side.

Add mutations to the root schema::

    import graphene
    import graphql_jwt


    class Mutation(graphene.ObjectType):
        delete_token_cookie = graphql_jwt.DeleteJSONWebTokenCookie.Field()

        # Long running refresh tokens
        delete_refresh_token_cookie = graphql_jwt.DeleteRefreshTokenCookie.Field()


    schema = graphene.Schema(mutation=Mutation)


* ``deleteTokenCookie`` to delete the ``JWT`` cookie:

  ::

      mutation {
        deleteTokenCookie {
          deleted
        }
      }

* ``deleteRefreshTokenCookie`` to delete ``JWT-refresh-token`` cookie for :doc:`long running refresh tokens<refresh_token>`.

  ::

      mutation {
        deleteRefreshTokenCookie {
          deleted
        }
      }

Per-argument
------------

Another option to send the *token* is using an argument within the *GraphQL* query, being able to send a batch of queries authenticated with different credentials.

*Django-graphql-jwt*  looks for the *token* in the list of arguments sent and if it does not exists, it looks for the token in the HTTP header.

Settings
~~~~~~~~

Enable the argument authentication in your settings:

::

    GRAPHQL_JWT = {
        "JWT_ALLOW_ARGUMENT": True,
    }


Schema
~~~~~~

Add the *token* argument in any of your fields using the same name defined in ``JWT_ARGUMENT_NAME`` setting::

    import graphene
    from graphql_jwt.decorators import login_required


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType, token=graphene.String(required=True))

        @login_required
        def resolve_viewer(self, info, **kwargs):
            return info.context.user


Queries
~~~~~~~

Send the token as another variable within the query:

::

    query GetViewer($token: String!) {
      viewer(token: $token) {
        username
        email
      }
    }


Authenticate using **multiple credentials**:

::

    query GetUsers($tokenA: String!, $tokenB: String!) {
      viewerA: viewer(token: $tokenA) {
        username
        email
      }
      viewerB: viewer(token: $tokenB) {
        username
        email
      }
    }
