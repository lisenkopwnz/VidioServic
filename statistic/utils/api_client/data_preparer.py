from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Self

from content.models.model_content import Content


@dataclass
class RecommendationDTO:
    """(Data Transfer Object) — класс, служащий для подготовки данных для дальнейшего использования
        в сервисе рекомендаций """
    title: str
    description: str
    pub_date_time: datetime
    rating: float
    categories_content: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self: Self)-> dict:
        """Возращает обект как словарь с корректной сериаизацией."""
        data = asdict(self)
        data["pub_date_time"] = self.pub_date_time.isoformat()  # Преобразование даты для дальнейшей сериализации
        return data

    @staticmethod
    def create(content: Content) -> "RecommendationDTO":
        """Метод используется для создания обекта dataclass """
        raise NotImplementedError
