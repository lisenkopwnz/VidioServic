from abc import ABC, abstractmethod


class AbstractApiClient(ABC):
    """
       Базовый абстрактный класс для клиентов взаимодействия с API.

       Этот класс задает общий интерфейс для отправки HTTP-запросов.
       Наследующие классы должны реализовать все абстрактные методы,
       чтобы определить логику взаимодействия с конкретным API.
    """

