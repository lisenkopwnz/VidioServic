from statistic.utils.api_client.base_api_client import AbstractApiClient


class FastAPIRecommendationClient(AbstractApiClient):

    @abstractmethod
    def send_request(self, method: str, endpoint: str, data=None, params=None):
        """Абстрактный метод для отправки запроса,
            должен быть реализован в дочерних классах"""

    @abstractmethod
    def build_url(self, endpoint: str) -> str:
        """
        Формирует полный URL для запроса, основываясь на базовом URL и конечной точке.
        """
        pass

    @abstractmethod
    def authenticate(self, headers: dict) -> dict:
        """
        Добавляет данные аутентификации в заголовки запроса.
        """
        pass

    @abstractmethod
    def handle_response(self, response):
        """
        Обрабатывает ответ от API, включая проверку статуса и парсинг данных.
        """
        pass
