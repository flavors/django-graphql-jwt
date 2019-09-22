from django.dispatch import Signal

refresh_token_revoked = Signal(providing_args=['request', 'refresh_token'])
refresh_token_rotated = Signal(providing_args=['request', 'refresh_token'])
