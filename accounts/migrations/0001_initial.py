# Generated by Django 5.1 on 2024-09-06 20:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0003_alter_content_author_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='content_statistic', serialize=False, to='content.content', verbose_name='Видиоконтент')),
                ('number_of_likes', models.PositiveIntegerField(default=0, verbose_name='Количество лайков')),
                ('number_of_dislikes', models.PositiveIntegerField(default=0, verbose_name='Количество дизлайков')),
                ('number_of_comments', models.PositiveIntegerField(default=0, verbose_name='Количество комментариев')),
                ('number_of_views', models.PositiveBigIntegerField(default=0, verbose_name='Количество просмотров')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='author_content', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Cтатистика',
                'verbose_name_plural': 'Cтатистика',
            },
        ),
    ]
