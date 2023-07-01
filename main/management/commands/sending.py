from django.core.management import BaseCommand

from main.services import send_email_to_clients


class Command(BaseCommand):
    """Запускает рассылку пользователям по команде из командной строки"""
    def handle(self, *args, **options):
        send_email_to_clients()