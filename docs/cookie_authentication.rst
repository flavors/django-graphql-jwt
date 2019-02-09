Cookie authentication
=====================

When a token is requested and ``jwt_cookie`` decorator is set, the response will set the given cookie with the token string::

    from django.urls import path

    from graphene_django.views import GraphQLView
    from graphql_jwt.decorators import jwt_cookie

    urlpatterns = [
        path('graphql/', jwt_cookie(GraphQLView.as_view())),
    ]


If the ``jwt_cookie`` decorator is set, consider adding `CSRF middleware <https://docs.djangoproject.com/es/2.1/ref/csrf/>`_ ``'django.middleware.csrf.CsrfViewMiddleware'`` to provide protection against `Cross Site Request Forgeries <https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)>`_.
