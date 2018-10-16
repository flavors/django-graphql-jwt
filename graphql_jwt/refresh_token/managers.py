from django.db import models
from django.db.models import Case, ExpressionWrapper, F
from django.db.models import Value as V
from django.db.models import When
from django.utils import timezone

from ..settings import jwt_settings


class RefreshTokenQuerySet(models.QuerySet):

    def expired(self):
        return self.annotate(
            expires=ExpressionWrapper(
                F('created') + V(jwt_settings.JWT_REFRESH_EXPIRATION_DELTA),
                output_field=models.DateTimeField(),
            ),
            expired=Case(
                When(expires__lt=timezone.now(), then=V(True)),
                output_field=models.BooleanField(),
                default=V(False),
            ),
        )
