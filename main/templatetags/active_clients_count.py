from django import template
from main.models import Clients
register = template.Library()


@register.simple_tag
def active_clients_count():
    count = Clients.objects.filter(is_active=True).count()
    return f'{count}'
