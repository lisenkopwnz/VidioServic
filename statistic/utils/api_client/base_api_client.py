from abc import ABC, abstractmethod
from typing import Any


class AbstractApiClient(ABC):
    """
    Базовый абстрактный класс для клиентов взаимодействия с API.

    Этот класс задает общий интерфейс для отправки HTTP-запросов.
    Наследующие классы должны реализовать все абстрактные методы,
    чтобы определить логику взаимодействия с конкретным API.
    """

    @abstractmethod
    def post(self) -> Any:
        """
        Абстрактный метод для отправки POST-запроса.
        """
        pass
