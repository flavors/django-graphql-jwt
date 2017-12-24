from calendar import timegm
from datetime import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

import graphene
from graphene.types.generic import GenericScalar

from . import settings
from .utils import get_payload, get_user_by_payload, jwt_encode, jwt_payload


class JWTMutationMixin(object):

    class Arguments:
        token = graphene.String()


class Verify(JWTMutationMixin, graphene.Mutation):
    payload = GenericScalar()

    @classmethod
    def mutate(cls, root, info, token, **args):
        payload = get_payload(token)
        return cls(payload=payload)


class Refresh(JWTMutationMixin, graphene.Mutation):
    data = GenericScalar()

    @classmethod
    def mutate(cls, root, info, token, **args):
        payload = get_payload(token)
        user = get_user_by_payload(payload)
        orig_iat = payload.get('orig_iat')

        if settings.JWT_VERIFY_REFRESH_EXPIRATION:
            if orig_iat:
                utcnow = timegm(datetime.utcnow().utctimetuple())
                expiration = orig_iat +\
                    settings.JWT_REFRESH_EXPIRATION_DELTA.total_seconds()

                if utcnow > expiration:
                    raise ValidationError(_('Refresh has expired'))
            else:
                raise ValidationError(_('orig_iat field is required'))

        refresh_payload = jwt_payload(user)
        refresh_payload['orig_iat'] = orig_iat

        return cls(data={
            'token': jwt_encode(refresh_payload),
            'payload': payload
        })
