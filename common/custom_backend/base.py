import logging
import time
from contextlib import contextmanager

from django.db.backends.postgresql.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.utils import CursorWrapper as DjangoCursorWrapper

logger = logging.getLogger('duration_request_view')


@contextmanager
def calc_sql_time(sql: str) -> None:
    """
    Контекстный менеджер для логирования времени выполнения SQL-запроса.

    :param sql: SQL-запрос, для которого будет логироваться время выполнения.
    """
    timestamp = time.monotonic()
    yield

    logger.info(
        f'Продолжительность SQL-запроса {sql} - '
        f'{time.monotonic() - timestamp:.3f} сек.'
    )


class CursorWrapper(DjangoCursorWrapper):
    def execute(self, sql: str, params: list = None) -> None:
        """
            Выполняет SQL-запрос и логирует его продолжительность.
        """
        with calc_sql_time(sql):
            return super().execute(sql, params)


class DatabaseWrapper(DjangoDatabaseWrapper):
    """
        Создает курсор для выполнения SQL-запросов.
    """

    def create_cursor(self, name: str = None) -> CursorWrapper:
        cursor = super().create_cursor(name)
        return CursorWrapper(cursor, self)
