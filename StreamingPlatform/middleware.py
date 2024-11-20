import logging
import time

logger = logging.getLogger('duration_request_view')


class LoggingMiddleware:
    """ Middleware использунтся для логирования продолжительности запросов к функциям
        и классам представления в приложениях. """

    def __init__(self, get_response: callable):
        """
        Инициализация middleware.

        :param get_response: Функция для обработки HTTP-запросов.
        """
        self._get_response = get_response

    def __call__(self, request):
        """
        Обработка входящего запроса.

        :param request: HTTP-запрос.
        :return: HTTP-ответ.
        """
        timestamp = time.monotonic()

        response = self._get_response(request)

        logger.info(
            f'Продолжительность запроса {request.path} - '
            f'{time.monotonic() - timestamp:.4f} сек.'
        )

        return response
