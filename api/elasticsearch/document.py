from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from django.contrib.auth import get_user_model

from StreamingPlatform import settings
from api.elasticsearch.analysis import analysis_settings
from content.models.model_content import Content


# Регистрация документа для индексации модели Content
@registry.register_document
class ContentDocument(Document):
    """
    Индекс для модели Content.
    """

    # Поля для индексации
    title = fields.TextField(
        fields={'raw': fields.KeywordField()},
    )
    description = fields.TextField()
    content = fields.KeywordField()
    preview_image = fields.KeywordField()
    slug = fields.KeywordField()
    pub_date_time = fields.DateField()
    is_private = fields.BooleanField()
    categories_content = fields.TextField(multi=True)
    author_content = fields.ObjectField(properties={
        'username': fields.KeywordField(),  # Убираем остальные поля и оставляем только username
    })

    class Index:
        # Имя индекса в Elasticsearch
        name = 'content'
        # Настройки индекса (необязательно, но полезно для производительности)
        # Должны во время развертывания на рабочем сервере быть изменены для отказоустойчивости
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'analysis': analysis_settings
        }

    class Django:
        model = Content  # Модель, с которой связан этот документ
        # Связанные модели
        related_models = [get_user_model()]

    @staticmethod
    def prepare_categories_content(instance):
        # Преобразуем категории в список строк (имена категорий)
        return [category.name for category in instance.categories_content.all()]

    @staticmethod
    def prepare_content(instance):
        """
        Возвращаем абсолютный URL к видеофайлу.
        Формируем полный URL, используя MEDIA_URL.
        """
        if instance.content:
            return settings.MEDIA_URL + instance.content.name
        return None

    @staticmethod
    def prepare_preview_image(instance):
        """
        Возвращаем абсолютный URL к изображению превью.
        Формируем полный URL, используя MEDIA_URL.
        """
        if instance.preview_image:
            return settings.MEDIA_URL + instance.preview_image.name
        return None
