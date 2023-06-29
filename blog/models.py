from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from transliterate import translit

NULLABLE = {'blank': True, 'null': True}

class Post(models.Model):
    """Класс для работы с моделью Постов"""
    name = models.CharField(max_length=150, verbose_name='заголовок')
    slug = models.CharField(max_length=150, unique=True,  verbose_name='slug')
    content = models.TextField(verbose_name='содержимое')
    image = models.ImageField(upload_to='post/', verbose_name='изображение', **NULLABLE)
    created_at = models.DateTimeField(verbose_name='дата создания', auto_now_add=True)
    published = models.BooleanField(verbose_name='признак публикации', default=True)
    view_count = models.PositiveIntegerField(verbose_name='количество просмотров', default=0)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        """Класс мета настроек"""
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('name','slug','-created_at',)
        permissions = [
            (
                'can_change_post',
                'Can change post'
            ),
        ]


    def increase_views(self):
        # Метод увеличивает количество просмотров
        self.view_count += 1
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            transliterated_title = translit(self.name, 'ru', reversed=True)
            self.slug = slugify(transliterated_title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})