import binascii
import os
from calendar import timegm

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from . import managers, signals
from ..settings import jwt_settings
from .shortcuts import create_refresh_token


@python_2_unicode_compatible
class AbstractRefreshToken(models.Model):
    id = models.BigAutoField(primary_key=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_token',
        verbose_name=_('user'))

    token = models.CharField(_('token'), max_length=255, editable=False)

    created = models.DateTimeField(_('created'), auto_now_add=True)
    revoked = models.DateTimeField(_('revoked'), null=True, blank=True)

    objects = managers.RefreshTokenQuerySet.as_manager()

    class Meta:
        abstract = True
        verbose_name = _('Refresh token')
        verbose_name_plural = _('Refresh tokens')
        unique_together = ('token', 'revoked')

    def __str__(self):
        return self.token

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        return super(AbstractRefreshToken, self).save(*args, **kwargs)

    def generate_token(self):
        return binascii.hexlify(
            os.urandom(jwt_settings.JWT_REFRESH_TOKEN_N_BYTES),
        ).decode()

    def is_expired(self, context=None):
        orig_iat = timegm(self.created.timetuple())
        return jwt_settings.JWT_REFRESH_EXPIRED_HANDLER(orig_iat, context)

    def revoke(self):
        self.revoked = timezone.now()
        self.save(update_fields=['revoked'])

        signals.refresh_token_revoked.send(
            sender=AbstractRefreshToken,
            refresh_token=self)

    def rotate(self):
        refresh_token = create_refresh_token(user=self.user)

        signals.refresh_token_rotated.send(
            sender=AbstractRefreshToken,
            refresh_token=self)

        return refresh_token


class RefreshToken(AbstractRefreshToken):
    """RefreshToken default model"""
