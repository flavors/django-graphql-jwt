import graphql

try:
    from graphql.execution.execute import GraphQLResolveInfo
except ImportError:
    from graphql.execution.base import ResolveInfo as GraphQLResolveInfo  # noqa


def get_root_type(info):
    if graphql.__version__.startswith("2"):
        return getattr(info.schema, f"get_{info.operation.operation}_type")()
    return getattr(info.schema, f"{info.operation.operation.value}_type")
