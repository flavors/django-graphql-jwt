from django.conf.urls import url

from graphene_django.views import GraphQLView

urlpatterns = [
    url(r'^$', GraphQLView.as_view(), name='index')
]
