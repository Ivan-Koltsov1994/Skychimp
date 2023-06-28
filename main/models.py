#Импортируем бибилотеку
from django.db import models

from config import settings

NULLABLE = {'blank': True, 'null': True}

class Clients(models.Model):
    """Класс для работы с моделью клиента сервиса"""
    name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    email = models.EmailField(max_length=150, verbose_name='почта', **NULLABLE)
    comment = models.TextField(verbose_name='комментарий', **NULLABLE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кем создан',
                                   related_name='client')

    # поле определения активных клиентов
    is_active = models.BooleanField(default=True, verbose_name='активный')

    def __str__(self):
        return f'{self.email} ({self.name})'


    class Meta:
        """Класс мета-настроек"""
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ('email',)  # сортировка, '-user' - сортировка в обратном порядке
        permissions = [
            (
                'can_view_client',
                'Can view client'
            ),
            (
                'can_block_client',
                'Can block client'
            ),
        ]


class Message(models.Model):
    """Класс для работы с моделью сообщения для рассылки"""
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    body = models.TextField(verbose_name='тело сообщения')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject

class Sending(models.Model):
    """Класс для работы с моделью настройки Рассылки """
    ONCE = 'Один раз'
    DAILY = '1 раз в день'
    WEEKLY = '1 раз в неделю'
    MONTHLY = '1 раз в месяц'

    FREQUENCY_CHOICES = [
        (ONCE, 'Один раз'),
        (DAILY, '1 раз в день'),
        (WEEKLY, '1 раз в неделю'),
        (MONTHLY, '1 раз в месяц'),
    ]

    CREATED = 'Создана'
    COMPLETED = 'Завершена'
    LAUNCHED = 'Запущена'

    SELECT_STATUS = [
        (CREATED, 'Создана'),
        (COMPLETED, 'Завершена'),
        (LAUNCHED, 'Запущена'),
    ]

    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_time = models.TimeField(auto_now_add=True, verbose_name='Время рассылки')
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, verbose_name='Периодичность')
    status = models.CharField(max_length=50, default='Создана', choices=SELECT_STATUS, verbose_name='Статус')
    created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Кем создано',
                                related_name='clients', **NULLABLE)

    def __str__(self):
        return f'ID: {self.id} - время рассылки: {self.scheduled_time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        permissions = [
            (
                'set_sending_status',
                'Can set sending status'
            ),
            (
                'can_view_sending',
                'Can view sending'
            ),
        ]


class Attempt(models.Model):
    """Класс для работы с моделью настройки попытки Рассылки"""
    DELIVERED = 'доставлено'
    NOT_DELIVERED = 'not_delivered'

    STATUS = (
        (DELIVERED, 'доставлено'),
        (NOT_DELIVERED, 'не доставлено'),
    )

    sending = models.ForeignKey(Sending, on_delete=models.CASCADE, verbose_name='Рассылка')
    sent_at = models.DateTimeField(auto_now_add=True, verbose_name='Время рассылки')
    status = models.CharField(choices=STATUS, verbose_name='Статус')
    response = models.TextField(**NULLABLE, verbose_name='Ответ сервера')

    def __str__(self):
        return f"{self.sending.message.subject} - {self.sent_at}"

    class Meta:
        verbose_name = 'Статистика (попытка)'
        verbose_name_plural = 'Статистики (попытки)'