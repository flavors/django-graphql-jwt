Cookie authentication
=====================

When a token is requested and ``jwt_cookie`` decorator is set, the response will set the given cookie with the token string::

    from django.urls import path

    from graphql_extensions.views import GraphQLView
    from graphql_jwt.decoratos import jwt_cookie

    urlpatterns = [
        path('graphql/', jwt_cookie(GraphQLView.as_view())),
    ]
