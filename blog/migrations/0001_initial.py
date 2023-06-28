# Generated by Django 4.2.1 on 2023-06-28 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='заголовок')),
                ('slug', models.CharField(max_length=150, unique=True, verbose_name='slug')),
                ('content', models.TextField(verbose_name='содержимое')),
                ('image', models.ImageField(blank=True, null=True, upload_to='post/', verbose_name='изображение')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('published', models.BooleanField(default=True, verbose_name='признак публикации')),
                ('view_count', models.PositiveIntegerField(default=0, verbose_name='количество просмотров')),
            ],
            options={
                'verbose_name': 'Пост',
                'verbose_name_plural': 'Посты',
                'ordering': ('name', 'slug', '-created_at'),
            },
        ),
    ]