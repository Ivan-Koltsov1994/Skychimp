from django import template
from django.core.mail import send_mail
from django.conf import settings
from main.models import Clients, Sending, Attempt, Message

register = template.Library()


def get_all_clients():
    """Получаем список всех клиентов для рассылки"""

    all_email = []  # Список всех email клиентов

    for сlient in Clients.objects.all():
        if сlient.is_active:
            all_email.append(str(сlient.email))  # заполняем активных клиентов в список
    return all_email


def send_email_to_clients(*args):
    """Отправляет рассылку клиентам"""

    status_list = []  # Список статусов отправки сообщения

    for send in Sending.objects.all():
        #проверяем периодичность отправки сообщения установленной в Crontab и статус сообщения
        if send.status == Sending.CREATED and send.frequency == (str(*args)):
            message_for_filter = send.message
            message_list = Message.objects.filter(subject=message_for_filter)
            for item in message_list:
                try:
                    send_mail(
                        subject=item.subject,
                        message=item.body,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[*get_all_clients()],
                    )

                    server_response = {
                        'sending': Sending.objects.get(pk=send.id),
                        'status': Attempt.DELIVERED,
                        'response': [*get_all_clients()]
                    }
                    status_list.append(Attempt(**server_response))
                    Attempt.objects.bulk_create(status_list)
                    print(f'Сообщение успешно отправлено {Sending.objects.get(pk=send.id)}')

                except Exception as e:
                    server_response = {
                        'sending': Sending.objects.get(pk=send.id),
                        'status': Attempt.NOT_DELIVERED,
                        'response': 'Ошибка при отправке сообщения: {}'.format(str(e)),
                    }
                    print(f'Ошибка при отправке сообщений {Sending.objects.get(pk=send.id)}')


                    status_list.append(Attempt(**server_response))
                    Attempt.objects.bulk_create(status_list)

                #Отправляем мгновенную рассылку при разовом значении
                if send.frequency == Sending.ONCE:
                    send.status = Sending.COMPLETED
                    send.save()
                else:
                    send.status = Sending.LAUNCHED
                    send.save()