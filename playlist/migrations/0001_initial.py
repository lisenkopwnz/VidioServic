# Generated by Django 5.1 on 2024-10-03 17:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('content', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Playlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_default=None, max_length=250, null=True, verbose_name='Название плейлиста')),
                ('author_playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_playlist', to=settings.AUTH_USER_MODEL, verbose_name='Автор плейлиста')),
                ('content', models.ManyToManyField(blank=True, related_name='content_playlist', to='content.content')),
            ],
        ),
    ]
