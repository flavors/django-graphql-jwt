from django.dispatch import Signal

token_issued = Signal(['request', 'user'])
token_refreshed = Signal(['request', 'user'])
