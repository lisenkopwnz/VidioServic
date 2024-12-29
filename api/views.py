from typing import List, Dict
from django.urls import URLPattern, get_resolver
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAdminUser])
def api_root_view(request) -> Response:
    """
    Представление, которое отвечает за отображение URL-адресов проекта.

    Это представление возвращает список всех маршрутов (эндпоинтов) проекта,
    включая их описания из строк документации (docstrings).

    Только администраторы могут получить доступ к этому представлению.
    """

    # Получение всех маршрутов проекта из текущего конфигурационного файла URL-адресов
    urlconf = get_resolver().url_patterns

    def get_paths(urlpatterns: List[URLPattern], parent_path: str = "") -> List[Dict[str, str]]:
        """
        Рекурсивно извлекает все пути и их описания из списка маршрутов.

        Args:
            urlpatterns (List[URLPattern]): Список маршрутов (уровень или вложенный).
            parent_path (str): Родительский путь для маршрутов (используется для вложенных маршрутов).

        Returns:
            List[Dict[str, str]]: Список словарей с информацией о маршрутах. Каждый словарь содержит:
                - 'path': Полный путь к маршруту.
                - 'description': Описание из строки документации (docstring) или сообщение по умолчанию.
        """
        endpoints = []

        # Обход всех маршрутов в текущем уровне
        for pattern in urlpatterns:
            if hasattr(pattern, "url_patterns"):  # Если маршрут является вложенным (include())
                nested_path = parent_path + str(pattern.pattern)  # Добавляем родительский путь
                endpoints.extend(get_paths(pattern.url_patterns, nested_path))  # Рекурсивный вызов
            elif hasattr(pattern, "pattern") and hasattr(pattern, "callback"):  # Если маршрут конечный
                callback = pattern.callback

                # Извлечение строки документации (docstring) из view (функции или класса)
                if hasattr(callback, "cls"):  # Если это class-based view
                    docstring = callback.cls.__doc__
                elif hasattr(callback, "__doc__"):  # Если это function-based view
                    docstring = callback.__doc__
                else:
                    docstring = "No documentation available"  # Если документации нет

                # Добавление информации о маршруте в список
                endpoints.append({
                    "path": f"{parent_path}{pattern.pattern}".replace("^", "").replace("$", ""),  # Полный путь
                    "description": docstring.strip() if docstring else "No documentation available",  # Описание
                })

        return endpoints

    # Получение всех эндпоинтов проекта
    endpoints = get_paths(urlconf)

    # Формирование ответа
    data = {
        "message": "API Project_video_servic!",
        "endpoints": endpoints
    }

    return Response(data, status=status.HTTP_200_OK)