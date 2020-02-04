Decorators
==========

@login_required
---------------

  .. autodata:: graphql_jwt.decorators.login_required

As a shortcut, you can use the ``login_required()`` decorator::

    import graphene
    from graphql_jwt.decorators import login_required


    class Query(graphene.ObjectType):
        viewer = graphene.Field(UserType)

        @login_required
        def resolve_viewer(self, info, **kwargs):
            return info.context.user

* If the user isn't logged in, raise ``PermissionDenied`` exception.
* If the user is logged in, execute the function normally.


@user_passes_test
-----------------

  .. autofunction:: graphql_jwt.decorators.user_passes_test

As a shortcut, you can use the convenient ``user_passes_test()`` decorator which raises a ``PermissionDenied`` exception when the callable returns ``False``::

    from django.contrib.auth import get_user_model

    import graphene
    from graphql_jwt.decorators import user_passes_test


    class Query(graphene.ObjectType):
        users = graphene.List(UserType)

        @user_passes_test(lambda user: user.email.contains('@staff'))
        def resolve_users(self, info, **kwargs):
            return get_user_model().objects.all()

``user_passes_test()`` takes a required argument: a callable that takes a ``User`` object and returns ``True`` if the user is allowed to perform the action. Note that ``user_passes_test()`` does not automatically check that the ``User`` is not anonymous.


@permission_required
--------------------

  .. autofunction:: graphql_jwt.decorators.permission_required

Decorator to check whether a user has a particular permission.

Just like the ``has_perm()`` method, permission names take the form::

    <app-label>.<permission-codename>

The decorator may also take an iterable of permissions, in which case the user must have all of the permissions in order to access the resolver or mutation::

    import graphene
    from graphql_jwt.decorators import permission_required

    class UpdateUser(graphene.Mutation):

        class Arguments:
            user_id = graphene.Int()

        @classmethod
        @permission_required('auth.change_user')
        def mutate(cls, root, info, user_id):
            ...


@staff_member_required
----------------------

  .. autodata:: graphql_jwt.decorators.staff_member_required

A resolver or mutation decorated with this function will having the following behavior:

If the user is a staff member (``User.is_staff=True``), execute the function normally.

Otherwise, the ``PermissionDenied`` exception will be raised::

    from django.contrib.auth import get_user_model

    import graphene
    from graphql_jwt.decorators import staff_member_required


    class Query(graphene.ObjectType):
        users = graphene.List(UserType)

        @staff_member_required
        def resolve_users(self, info, **kwargs):
            return get_user_model().objects.all()


@superuser_required
-------------------

  .. autodata:: graphql_jwt.decorators.superuser_required

A resolver or mutation decorated with this function will having the following behavior:

If the user is superuser (``User.is_superuser=True``), execute the function normally.

Otherwise, the ``PermissionDenied`` exception will be raised::

    import graphene
    from graphql_jwt.decorators import superuser_required


    class DeleteUser(graphene.Mutation):

        class Arguments:
            user_id = graphene.Int()

        @classmethod
        @superuser_required
        def mutate(cls, root, info, user_id):
            ...
