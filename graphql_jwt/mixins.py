from calendar import timegm
from datetime import datetime

from django.utils.translation import ugettext_lazy as _

import graphene
from graphene.types.generic import GenericScalar

from . import exceptions, settings
from .shortcuts import get_token
from .utils import get_payload, get_user_by_payload


class VerifyMixin(object):
    payload = GenericScalar()


class RefreshMixin(object):
    token = graphene.String()
    payload = GenericScalar()

    @classmethod
    def refresh(cls, root, info, token, **kwargs):
        payload = get_payload(token)
        user = get_user_by_payload(payload)
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            utcnow = timegm(datetime.utcnow().utctimetuple())
            expiration = orig_iat +\
                settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()

            if utcnow > expiration:
                raise exceptions.GraphQLJWTError(_('Refresh has expired'))
        else:
            raise exceptions.GraphQLJWTError(_('orig_iat field is required'))

        token = get_token(user, orig_iat=orig_iat)
        return cls(token=token, payload=payload)
