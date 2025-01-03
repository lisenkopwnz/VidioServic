from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Self

from content.models.model_content import Content


@dataclass
class RecommendationDTO:
    """(Data Transfer Object) — класс, служащий для подготовки данных для дальнейшего использования
        в сервисе рекомендаций """
    slug: str
    title: str
    description: str
    pub_date_time: datetime
    rating: float
    categories_content: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    def to_dict(self: Self)-> dict:
        """Возращает обект как словарь с корректной сериаизацией."""
        data = asdict(self)
        # Преобразование даты для дальнейшей сериализации
        data["pub_date_time"] = self.pub_date_time.isoformat()
        return data

    @staticmethod
    def create(content: Content) -> "RecommendationDTO":
        """Метод используется для создания обекта dataclass """
        rating = content.content_statistic.rating if hasattr(content, 'content_statistic') else 0.0
        return RecommendationDTO(
            slug=content.slug,
            title=content.title,
            description=content.description,
            pub_date_time=content.pub_date_time,
            rating=rating,
            categories_content=list(content.categories_content.values_list('name', flat=True)),
            tags=content.tags
        )
