from django.dispatch import Signal

# providing_args=['request', 'refresh_token']
refresh_token_revoked = Signal()

# providing_args=['request', 'refresh_token', 'refresh_token_issued']
refresh_token_rotated = Signal()
