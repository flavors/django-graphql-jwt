from django.core.management.base import BaseCommand

from graphql_jwt.refresh_token.blacklist import set_blacklist

from ...utils import get_refresh_token_model


class Command(BaseCommand):
    help = 'Build initial blacklist'

    def handle(self, *args, **options):
        for refresh_token in get_refresh_token_model().objects.filter(revoked__isnull=False):
            set_blacklist(refresh_token)
