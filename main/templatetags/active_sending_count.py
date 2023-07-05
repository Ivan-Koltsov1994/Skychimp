from django import template
from main.models import Sending
register = template.Library()

@register.simple_tag
def active_sending_count():
    send_count = Sending.objects.filter(status=Sending.LAUNCHED).count()
    return f'{send_count} рассылки'