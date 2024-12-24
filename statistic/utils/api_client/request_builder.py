import os
from typing import Dict, Any

import httpx
from dotenv import load_dotenv

load_dotenv()

class HttpxClientBuilder:
    def __init__(
            self,
            base_url: str,
            timeout_connect: int = 5,
            timeout_read: int = 10,
            timeout_write:int = 5.0,
            verify_ssl:bool = True
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
        api_key = os.getenv("API_KEY")
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
                return response.json()
        except httpx.TimeoutException:
            pass
        except httpx.RequestError as e:
            pass
        except httpx.HTTPStatusError as e:
            pass

        return None
