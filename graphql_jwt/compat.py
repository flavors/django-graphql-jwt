try:
    from graphql.execution.execute import GraphQLResolveInfo
except ImportError:
    from graphql.execution.base import ResolveInfo as GraphQLResolveInfo  # noqa


def get_operation_name(operation):
    if hasattr(operation, "value"):
        return operation.value
    return operation
