# Generated by Django 5.1 on 2024-10-27 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription_active',
            field=models.BooleanField(default=False, verbose_name='Статус подписки на закрытый котент'),
        ),
    ]
