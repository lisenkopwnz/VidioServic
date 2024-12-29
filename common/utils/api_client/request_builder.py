from typing import Dict, Any
import httpx

from StreamingPlatform.settings import API_KEY
from common.utils.api_client.exceptions import ApiClientException


class HttpxClientBuilder:
    """Низкоуровневое API для создания запроса"""
    def __init__(
            self,
            base_url: str,
            timeout_connect: int,
            timeout_read: int,
            timeout_write: int,
            verify_ssl: bool
            ):
        """
        Инициализация HTTPX клиента с базовым URL и временем ожидания.
        :param base_url: базовый URL API.
        :param timeout_connect: время ожидания для установления соединения.
        :param timeout_read: время ожидания для чтения данных.
        :param timeout_write: время ожидания для записи данных.
        """
        self.base_url = base_url
        self.timeout = httpx.Timeout(connect=timeout_connect,  #создаем универсальный таймаут для различных операций
                                     read=timeout_read,
                                     write=timeout_write)
        self.verify_ssl = verify_ssl

    @staticmethod
    def __get_api_key():
        """
            Формирует и возвращает заголовки HTTP-запроса с API-ключом для авторизации.

            Этот метод создает заголовок `Authorization` с использованием API-ключа в формате `Bearer Token`.
            API-ключ берется из глобальной переменной `API_KEY`.
        """
        api_key = API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        return headers

    def _build_url(self, endpoint: str)-> str:
        """
        Строит полный URL для запроса.
        :param endpoint: конечная часть URL.
        :returns: полный URL.
        """
        return f'{self.base_url}/{endpoint}'

    def send_post_request(self,endpoint: str, data: Dict[str, Any])-> Any:
        """
        Отпровляет POST-запрос с данными на указанный адрес с данными, используя контекстный менеджер.
        :param endpoint: конечная часть URL.
        :param data: данные для отправки.
        :return: ответ от сервера.
        """
        try:
            url = self._build_url(endpoint)
            headers = HttpxClientBuilder.__get_api_key()
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=data, headers=headers)
                response.raise_for_status()  #проверка на успешный статус (2xx)
                return response
        except httpx.TimeoutException as e:
            raise ApiClientException(
                message=f'Ошибка: превышен тайм-аут при подключении или ожидании ответа: {str(e)}',
                error_code="TIMEOUT",
            )
        except httpx.RequestError as e:
            raise ApiClientException(
                f'Ошибка запроса: {str(e)}',
                error_code="REQUEST_ERROR",
            )
        except httpx.HTTPStatusError as e:
            raise ApiClientException(
                f'Ошибка HTTP: {str(e)}',
                error_code=e.response.status_code,
            )
