import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin


class Refresh(RefreshTokenMixin, graphql_jwt.Refresh):
    class Arguments(RefreshTokenMixin.Fields):
        """Refresh Arguments"""
