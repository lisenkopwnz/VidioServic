from dataclasses import field
from datetime import datetime

from attr import dataclass

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

    @staticmethod
    def create(recommendation: Content) -> "RecommendationDTO":
        """Метод используется для создания обекта dataclass """
        NotImplemented
