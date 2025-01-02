from typing import Dict, Any

from StreamingPlatform.settings import RECOMMENDATION_SERVICE_URL
from common.utils.api_client.base_api_client import AbstractApiClient
from common.utils.api_client.request_builder import HttpxClientBuilder
from content.models.model_content import Content


class ContentBasedRecommendationsClient(AbstractApiClient):
    """
    Класс для получения рекомендаций контента, похожего на просматриваемый.

    Этот класс взаимодействует с API рекомендаций и предоставляет методы для получения
    контента, который похож на текущий просматриваемый контент. Рекомендации могут быть
    основаны на различных критериях, таких как жанр, теги, рейтинг или поведение пользователей.

    Все параметры, кроме `base_url`, являются необязательными.

    :param base_url: Базовый URL API (по умолчанию RECOMMENDATION_SERVICE_URL).
    :param endpoint: Конечный эндпоинт API (обязательный).
    :param data: Данные которые будут отправленны (обязательный).
    :param timeout_connect: Время ожидания для установления соединения в секундах (по умолчанию 5).
    :param timeout_read: Время ожидания для чтения данных в секундах (по умолчанию 10).
    :param timeout_write: Время ожидания для записи данных в секундах (по умолчанию 5.0).
    :param verify_ssl: Включение или отключение SSL-верификации (по умолчанию True).

    Основные функции:
    - Получение списка контента, похожего на указанный.

    Пример использования:
        >>> content = Content(
        ...     id="789",
        ...     title="Example Content",
        ...     description="This is an example content.",
        ...     categories=["movies", "drama"]
        ...     ...
        ...     )
        >>> client = ContentBasedRecommendationsClient(
        ...     base_url="https://api.example.com",
        ...     endpoint="similar-content",
        ...     content=content
        ... )
        >>> similar_content = client.post()
    """
    def __init__(
            self,
            endpoint: str,
            data: Dict[str,Any],
            base_url: str = RECOMMENDATION_SERVICE_URL,
            timeout_connect: int = 5,
            timeout_read: int = 10,
            timeout_write: int = 5,
            timeout_pool: int = 5,
            verify_ssl: bool = True
    ):
        self.client = HttpxClientBuilder(
            base_url,
            timeout_connect,
            timeout_read,
            timeout_write,
            timeout_pool,
            verify_ssl,
        )
        self.endpoint = endpoint
        self.data = data

    def post(self):
        """Отправляет запрос на API для получения рекомендаций """
        response = self.client.send_post_request(self.endpoint,self.data)
        return response.json()
