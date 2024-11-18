from rest_framework.pagination import PageNumberPagination


class ContentPaginator(PageNumberPagination):
    page_size = 50  # Количество элементов на одной странице
    max_page_size = 100  # Максимальный размер страницы
    page_query_param = 'page'  # Параметр для страницы
    page_size_query_param = 'page_size'  # Параметр для размера страницы

    def paginate_queryset(self, queryset, request, view=None):
        """
        Пагинируем результат запроса, полученный от Elasticsearch (в формате JSON).
        """
        if queryset is None or not isinstance(queryset, dict):
            return None

        # Извлекаем общую информацию о 'hits' из ответа Elasticsearch
        hits = queryset.get('hits', {}).get('hits', [])
        total_count = queryset.get('hits', {}).get('total', {}).get('value', 0)

        # Получаем параметры пагинации из запроса
        page_size = self.get_page_size(request)  # Количество элементов на странице
        page_number = self.paginate_queryset_page(request)  # Текущая страница

        # Вычисляем начальный и конечный индекс для пагинации
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size

        # Ограничиваем количество результатов на странице
        paginated_data = hits[start_index:end_index]

        # Формируем ответ с данными для пагинации
        return self.get_paginated_response(paginated_data)

    def get_paginated_response(self, data):
        """
        Формируем ответ с данными и информацией о пагинации.
        """
        return {
            'count': len(data),  # Общее количество элементов на странице
            'next': self.get_next_link(),  # Следующая страница
            'previous': self.get_previous_link(),  # Предыдущая страница
            'results': data  # Результаты на текущей странице
        }

    def paginate_queryset_page(self, request):
        """
        Возвращает номер текущей страницы, учитывая параметр запроса.
        """
        page = request.query_params.get(self.page_query_param, 1)

        return int(page)
