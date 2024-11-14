import django_filters
from .models.model_content import Content

class ContentFilter(django_filters.FilterSet):
    categories_content = django_filters.CharFilter(method='filter_by_categories', label='Категории')

    @staticmethod
    def filter_by_categories(queryset, name, value):
        """
        Фильтруем по категориям, получаемым из запроса.
        В Elasticsearch используется фильтрация через `terms`.
        """
        categories = [cat.strip() for cat in value.split(',') if cat.strip()]

        if categories:
            # Фильтрация по полям `categories_content` в Elasticsearch
            # Используем оператор `terms` для фильтрации по списку категорий
            queryset = queryset.filter("terms", categories_content__name=categories)

        return queryset

    class Meta:
        model = Content
        fields = ['categories_content']

class SearchFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Поиск')

    @staticmethod
    def filter_search(queryset, name, value):
        """
        Фильтруем по категориям, получаемым из запроса.
        В Elasticsearch используется фильтрация через `terms`.
        """
        categories = [cat.strip() for cat in value.split(',') if cat.strip()]

        if categories:
            # Фильтрация по полям `categories_content` в Elasticsearch
            # Используем оператор `terms` для фильтрации по списку категорий
            queryset = queryset.filter("terms", categories_content__name=categories)

        return queryset
