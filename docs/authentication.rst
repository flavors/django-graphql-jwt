Authentication
==============

*Django-graphql-jwt* uses a `Graphene middleware <https://docs.graphene-python.org/en/latest/execution/middleware/>`_ to hook the authenticated user into *context* object. The simple, raw way to limit access to data is to check ``info.context.user.is_authenticated``::

    import graphene


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)

        def resolve_viewer(self, info, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise Exception('Authentication credentials were not provided')
            return user


As a shortcut, you can use :doc:`decorators<decorators>` for your *resolvers* and *mutations*.


HTTP header
-----------

Now in order to access protected API you must include the ``Authorization`` HTTP header.

.. code-block:: http

    POST / HTTP/1.1
    Host: domake.io
    Authorization: JWT <token>
    Content-Type: application/json;


Per-argument
------------

Another option to send the *token* is using an argument within the *GraphQL* query, being able to send a batch of queries authenticated with different credentials.

*Django-graphql-jwt*  looks for the *token* in the list of arguments sent and if it does not exists, it looks for the token in the HTTP header.

Settings
~~~~~~~~

Enable the argument authentication in your settings:

::

    GRAPHQL_JWT = {
        'JWT_ALLOW_ARGUMENT': True,
    }


Schema
~~~~~~

Add the *token* argument in any of your fields using the same name defined in ``JWT_ARGUMENT_NAME`` setting::

    import graphene
    from graphql_jwt.decorators import login_required


    class Query(graphene.ObjectType):
        graphene.Field(UserType, token=graphene.String(required=True))

        @login_required
        def resolve_viewer(self, info, **kwargs):
            return info.context.user


Queries
~~~~~~~

Send the token as another variable within the query:

::

    mutation GetViewer($token: String!) {
      viewer(token: $token) {
        id
        username
        email
      }
    }
