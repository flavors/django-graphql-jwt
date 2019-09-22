from django.dispatch import Signal

token_issued = Signal(providing_args=['request', 'user'])
token_refreshed = Signal(providing_args=['request', 'user'])
