from django.core.management.base import BaseCommand

from ...utils import get_refresh_token_model
from graphql_jwt.refresh_token.blacklist import set_blacklist


class Command(BaseCommand):
    help = 'Build initial blacklist'

    def handle(self, expired, *args, **options):
        for refresh_token in get_refresh_token_model().objects.filter(revoked__isnull=False):
            set_blacklist(refresh_token)
