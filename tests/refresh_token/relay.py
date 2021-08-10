import graphql_jwt
from graphql_jwt.refresh_token.mixins import RefreshTokenMixin


class Refresh(RefreshTokenMixin, graphql_jwt.relay.Refresh):
    class Input(RefreshTokenMixin.Fields):
        """Refresh Input"""
