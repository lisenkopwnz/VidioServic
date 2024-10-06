# Generated by Django 5.1 on 2024-10-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('payment_options', models.CharField(choices=[('PP', 'paypal'), ('ST', 'stripe'), ('PM', 'payme')], max_length=50, verbose_name='Способ оплаты')),
                ('status', models.CharField(choices=[('P', 'Ожидание'), ('C', 'Завершено'), ('F', 'Не выполнено')], default='P', max_length=2, verbose_name='Статус')),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='ID Транзакции')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Платёж',
                'verbose_name_plural': 'Платежи',
                'ordering': ('-created_at',),
            },
        ),
    ]
