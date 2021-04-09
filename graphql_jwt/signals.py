from django.dispatch import Signal

# providing_args=['request', 'user']
token_issued = Signal()

# providing_args=['request', 'user']
token_refreshed = Signal()
