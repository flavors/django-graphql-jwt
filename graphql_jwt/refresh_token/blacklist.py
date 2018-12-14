from django.core.cache import cache
from django.utils import timezone

from ..settings import jwt_settings

JWT_BLACKLIST_KEY = jwt_settings.JWT_CACHE_PREFIX + "/blacklist/%s"


def set_blacklist(refresh_token_obj):
    key = JWT_BLACKLIST_KEY % refresh_token_obj.token
    # Add 10 seconds - just to be sure
    expire = int((timezone.now() - refresh_token_obj.created + jwt_settings.JWT_REFRESH_EXPIRATION_DELTA).total_seconds()) + 10
    cache.set(key, expire)


def is_in_blacklist(refresh_token):
    key = JWT_BLACKLIST_KEY % refresh_token
    return cache.get(key, default=False)
