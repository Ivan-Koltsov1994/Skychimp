# Generated by Django 4.2.1 on 2023-06-29 14:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('name', 'slug', '-created_at'), 'permissions': [('can_change_post', 'Can change post')], 'verbose_name': 'Пост', 'verbose_name_plural': 'Посты'},
        ),
    ]
