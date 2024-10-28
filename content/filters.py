import django_filters
from .models.model_content import Content


class ContentFilter(django_filters.FilterSet):
    categories_content = django_filters.CharFilter(method='filter_by_categories', label='Категории')

    @staticmethod
    def filter_by_categories(queryset, name, value):
        # Разбиваем строку по запятой и очищаем пробелы
        categories = [cat.strip() for cat in value.split(',') if cat.strip()]
        if categories:
            # Фильтруем по всем указанным категориям
            queryset = queryset.filter(categories_content__name__in=categories).distinct()
        return queryset

    class Meta:
        model = Content
        fields = ['categories_content']
