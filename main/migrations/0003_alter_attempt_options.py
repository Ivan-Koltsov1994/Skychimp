# Generated by Django 4.2.1 on 2023-06-28 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attempt',
            options={'verbose_name': 'Статистика (попытка)', 'verbose_name_plural': 'Статистики (попытки)'},
        ),
    ]
