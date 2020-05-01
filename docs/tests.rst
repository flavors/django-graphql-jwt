Writing tests
-------------

  .. autoclass:: graphql_jwt.testcases.JSONWebTokenTestCase

This package includes a subclass of `unittest.TestCase <https://docs.python.org/3/library/unittest.html#unittest.TestCase>`_ and improve support for making *GraphQL* queries using *JSON Web Token* authentication::

    from django.contrib.auth import get_user_model

    from graphql_jwt.testcases import JSONWebTokenTestCase


    class UsersTests(JSONWebTokenTestCase):

        def setUp(self):
            self.user = get_user_model().objects.create(username='test')
            self.client.authenticate(self.user)

        def test_get_user(self):
            query = '''
            query GetUser($username: String!) {
              user(username: $username) {
                id
              }
            }'''

            variables = {
              'username': self.user.username,
            }

            executed = self.client.execute(query, variables)
            
            assert expected == {
              'data': {
                'user': {
                  'id': 0
                }
              }
            }
