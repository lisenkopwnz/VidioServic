# Generated by Django 5.1 on 2024-10-27 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_content_is_private_content_preview_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='preview_image',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='preview/$Y/%m/%d/', verbose_name='Превью'),
        ),
    ]
