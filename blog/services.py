from django.core.mail import send_mail
from django.conf import settings

from blog.models import Post


def send_post_email(post_item: Post):
    send_mail(
        f'Пост {post_item.name} набрал 100 просмотров ',
        'Поздравляю! Ваша запись пользуется популярностью!',
        settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER]
    )
