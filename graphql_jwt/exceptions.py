from django.utils.translation import ugettext_lazy as _


class GraphQLJWTError(Exception):
    default_message = None

    def __init__(self, message=None):
        if message is None:
            message = self.default_message

        super(GraphQLJWTError, self).__init__(message)


class PermissionDenied(GraphQLJWTError):
    default_message = _('You do not have permission to perform this action')
